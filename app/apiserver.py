import datetime
import json
import logging

import os
import requests
from eve import Eve
from flask import request, jsonify, current_app, render_template, abort, session
from flask_babelex import Babel
from jwt import DecodeError
from mongoengine import connect
from raven.contrib.flask import Sentry
from werkzeug.utils import redirect

from Documents.patient import Patient, PatientIdSeed
from Documents.testdata import Testdata
from app.extensions import admin, login_manager
from app.helper.dataprocessing import load_patient_info
from app.auth.token import jwt
from app.user.models import User
import jwt as jwt_package

sentry = Sentry(
    dsn='https://5be8a37ac67e46e49ac06fae5f387309:60f1c341ba6f4fdda945b23abb3099b8@sentry.io/1276358')


def on_insert_testdata_callback(items):
    for item in items:
        test = item['test']
        patient_info = test['patient_info']
        if not patient_info['patient_id']:
            patient_info.pop("patient_id")
            seed = PatientIdSeed.objects.first()
            while not seed.modify(inc__counter=1):
                continue
            patient = Patient(patient_id=str(seed.counter))
        else:
            patient = Patient.objects(patient_id=patient_info['patient_id']).first()
            if patient is None:
                patient = Patient(patient_id=patient_info['patient_id'])
        load_patient_info(patient, patient_info)
        patient.save()
        item['patient_id'] = patient.patient_id
        # bring result out to the root level
        item['result'] = item['test']['result']


def human_correction():
    item = request.get_json()
    test_id = item['test_id']
    patient_info = item.get("patient_info", None)
    if patient_info:
        patient = Patient.objects(patient_id=patient_info['patient_id']).first()
        testdata = Testdata.objects(id=test_id).first()
        if patient is None or testdata is None:
            return jsonify({'_status': 'Not found'}), 404
        load_patient_info(patient, patient_info)
        testdata.test['patient_info'] = patient_info
        testdata.save()
        patient.save()

    corrections = item['corrections']

    human_correction_backend(test_id, corrections)
    return jsonify({'_status': 'OK'}), 200


def human_correction_backend(test_id, corrections):
    testdata = Testdata.objects(id=test_id).first()
    if testdata is None:
        raise FileNotFoundError("testdata with id {0} cannot be found in the database".format(test_id))
    for i in corrections:
        correctness = int(corrections[i]) == int(testdata.test['vas_cog_block'][i]['vas_ques'])
        testdata.test['result'][i] = correctness
        testdata.result[i] = correctness  # update root level result as well
        print('Block {0} correction {1} against vasQues {2} is:{3}'.format(i,
                                                                           corrections[i],
                                                                           testdata.test['vas_cog_block'][i][
                                                                               'vas_ques'],
                                                                           str(correctness))
              )
    testdata.human_correction = corrections
    testdata.save(write_concern={'w': 1, 'fsync': True})


def on_fetched_item_testdata_callback(response):
    patient_info = Patient.objects(patient_id=response['patient_id']).first()
    residue = response['test']['patient_info']
    response['test']['patient_info'] = patient_info.to_mongo()
    response['test']['patient_info']['patient_id'] = response['test']['patient_info'].pop('_id')
    residue_items = ['high_blood_pressure', 'setting_of_assessment', 'assessment_date_calendar', 'visit',
                     'current_medications', 'mmse_score', 'assessment_date', 'moca_score', 'diabetes_mellitus',
                     'high_cholesterol', 'diagnosis', 'charleston_scale', 'note', 'sarc_f']
    # for some items in the patient info we don't want to see the latest but the time when they take the test
    for item in residue_items:
        if residue.get(item, None):
            response['test']['patient_info'][item] = residue[item]


def add_timestamp(response):
    for item in response['_items']:
        item['_updated_total_seconds'] = (item['updated_at'] - datetime.datetime(1970, 1, 1)).total_seconds()


def configure_extensions(server):
    jwt.init_app(server)
    import app.admin.views
    admin.init_app(server)
    login_manager.init_app(server)
    sentry.init_app(server)
    babel = Babel(server)

    @babel.localeselector
    def get_locale():
        if request.args.get('lang'):
            session['lang'] = request.args.get('lang')
        return session.get('lang', 'en')


def create_server(test=False):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    server = ApiServer(template_folder=dir_path + '/templates', static_folder=dir_path +
                                                                              '/static',
                       root_path=dir_path, settings=dir_path + '/../settings.py')
    if test:
        server.config.from_object('app.config.TestingConfig')
    else:
        server.config.from_object('app.config.DevelopmentConfig')
    server.configure()
    configure_error_handlers(server)
    configure_extensions(server)
    return server


class ApiServer(Eve):
    """
        Workaround for https://github.com/pyeve/eve/issues/1087
        """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection = None

    def __getattr__(self, name):
        if name in {"im_self", "im_func"}:
            raise AttributeError("type object '%s' has no attribute '%s'" %
                                 (self.__class__.__name__, name))
        return super(ApiServer, self).__getattr__(name)

    def configure(self):
        self.on_insert_testdata += on_insert_testdata_callback
        self.on_fetched_item_testdata += on_fetched_item_testdata_callback
        self.on_fetched_resource_testlist += add_timestamp
        self.add_url_rule('/mark_one', 'mark_one', mark_one, methods=['POST'])
        self.add_url_rule('/bootstrap', 'bootstrap', bootstrap, methods=['GET'])
        self.add_url_rule('/humancorrection', 'humancorrection', human_correction, methods=['POST'])
        self.add_url_rule('/checkversion', 'checkversion',  check_current_apk_version, methods=['GET'])
        logHandler = logging.FileHandler('app.log')
        logHandler.setLevel(logging.INFO)
        self.logger.addHandler(logHandler)
        self.logger.setLevel(logging.INFO)
        mongo_username = self.config.get('MONGO_USERNAME', None)
        mongo_password = self.config.get('MONGO_PASSWORD', None)
        self.connection = connect('eve', username=mongo_username, password=mongo_password)


def mark_one():
    raise NotImplementedError()
    raw_data = request.get_json()
    response = requests.post(current_app.config['MARKER_API_URL'] + 'mark_one', json=raw_data)
    return jsonify(json.loads(response.text))


def bootstrap():
    user = User()
    user.username = 'admin'
    user.password = '123456'
    user.display_name = 'master'
    user.save()


def configure_error_handlers(server):
    @server.errorhandler(DecodeError)
    def jwt_decode_error_handler(error):
        return 'JWT decode error: ' + str(error), 401

    @server.errorhandler(jwt_package.ExpiredSignatureError)
    def jwt_signature_expired_handler(error):
        return 'Signature expired. Please log in again.', 401

    @server.errorhandler(jwt_package.InvalidTokenError)
    def jwt_invalid_token_handler(error):
        return 'Invalid token. Please log in again.', 401

    @server.errorhandler(403)
    def access_forbidden(error):
        return render_template('error.html', message=str(error))

    @server.errorhandler(401)
    def unauthorized_error_handler(error):
        return redirect("/login")


def check_current_apk_version():
    base_dir = '/home/www'
    sub_dir = '/static'
    static_dir = base_dir + sub_dir
    namelist = os.listdir(static_dir)
    name = ""
    for filename in namelist:
        if filename.__contains__("SDMT"):
            name = filename
    version = name.replace(".apk", "").replace("SDMT", "")
    update_info = {'_version_num': version, "_download_url" : sub_dir + "/" + name}
    with open(static_dir+'/appreadme.txt') as f:
        release_notes = f.read()
        update_info['_release_note'] = release_notes
    return jsonify(update_info), 200
