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

from Documents.patient import Patient
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

        patient = Patient.objects(patient_id=patient_info['patient_id']).first()
        if patient is None:
            patient = Patient(patient_id=patient_info['patient_id'])
        load_patient_info(patient, patient_info)
        patient.save()
        item['patient_id'] = patient.id
        # bring result out to the root level
        item['result'] = item['test']['result']


def human_correction():
    item = request.get_json()
    test_id = item['test_id']
    corrections = item['corrections']

    human_correction_backend(test_id, corrections)
    return jsonify({'_status': 'OK'}), 200


def human_correction_backend(test_id, corrections):
    testdata = Testdata.objects(id=test_id).first()
    if testdata is None:
        raise FileNotFoundError("testdata with id {0} cannot be found in the database".format(test_id))
    for i in corrections:
        correctness = corrections[i] == testdata.test['vas_cog_block'][i]['vas_ques']
        testdata.test['result'][i] = str(correctness)
        testdata.result[i] = str(correctness)  # update root level result as well
        print('Block {0} correction {1} against vasQues {2} is:{3}'.format(i,
                                                                           corrections[i],
                                                                           testdata.test['vas_cog_block'][i][
                                                                               'vas_ques'],
                                                                           str(correctness))
              )
    testdata.human_correction = corrections
    testdata.save(write_concern={'w': 1, 'fsync': True})


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


def create_server():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    server = ApiServer(template_folder=dir_path + '/templates', static_folder=dir_path +
                                                                              '/static',
                       root_path=dir_path)
    server.config.from_object('app.config.DevelopmentConfig')
    server.configure()
    configure_error_handlers(server)
    configure_extensions(server)
    return server


class ApiServer(Eve):
    """
        Workaround for https://github.com/pyeve/eve/issues/1087
        """

    def __getattr__(self, name):
        if name in {"im_self", "im_func"}:
            raise AttributeError("type object '%s' has no attribute '%s'" %
                                 (self.__class__.__name__, name))
        return super(ApiServer, self).__getattr__(name)

    def configure(self):
        self.on_insert_testdata += on_insert_testdata_callback
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
        connect('eve', username=mongo_username, password=mongo_password)


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
