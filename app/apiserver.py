import datetime
import json
import logging

import os
import requests
from eve import Eve
from flask import request, jsonify, current_app, render_template
from jwt import DecodeError
from mongoengine import connect

from Documents.patient import Patient
from Documents.testdata import Testdata
from app.extensions import admin, login_manager
from app.helper.dataprocessing import load_patient_info
from app.auth.token import jwt
from app.user.models import User
import jwt as jwt_package


def on_insert_testdata_callback(items):
    for item in items:
        test = item['test']
        patient_info = test['patientInfo']
        vas_block_size = test['vasBlockSize']
        vas_cog_block = test['vasCogBlock']
        response = requests.post(current_app.config['MARKER_API_URL'] + 'mark', json={'vasCogBlock': vas_cog_block,
                                                                                      'vasBlockSize': vas_block_size})
        item['result'] = json.loads(response.text)
        patient = Patient.objects(patient_id=patient_info['patientId']).first()
        if patient is None:
            patient = Patient(patient_id=patient_info['patientId'])
        load_patient_info(patient, patient_info)
        patient.save()
        item['patient_id'] = patient.id
        item['patient_name'] = patient_info['patientName']


def on_inserted_humancorrection_callback(request,lookup):
    test_id = lookup['_id']
    corrections = request.json['human_correction']

    testdata = Testdata.objects(id=test_id).first()
    if testdata is None:
        raise FileNotFoundError("testdata with id {0} cannot be found in the database".format(test_id))
    for i in corrections:
        correctness = corrections[i] == testdata.test['vasCogBlock'][i]['vasQues']
        testdata.result[i] = str(correctness)
        print('Block {0} correction {1} against vasQues {2} is:{3}'.format(i,
              corrections[i],
              testdata.test['vasCogBlock'][i]['vasQues'],
              str(correctness))
              )
    testdata.save(write_concern={'w': 1, 'fsync': True})


def on_fetched_item_testdata_callback(response):
    print(response['result'])


def add_timestamp(response):
    for item in response['_items']:
        item['_updated_total_seconds'] = (item['updated_at'] - datetime.datetime(1970, 1, 1)).total_seconds()


def configure_extensions(server):
    jwt.init_app(server)
    import app.admin.views
    admin.init_app(server)
    login_manager.init_app(server)


def create_server():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    server = ApiServer(template_folder=dir_path+'/templates')
    server.config.from_object('app.config.DevelopmentConfig')
    server.configure()
    configure_error_handlers(server)
    configure_extensions(server)
    return server


class ApiServer(Eve):
    def configure(self):
        self.on_insert_testdata += on_insert_testdata_callback
        self.on_pre_PATCH_testdata += on_inserted_humancorrection_callback
        self.on_fetched_item_testdata += on_fetched_item_testdata_callback
        self.on_fetched_resource_testlist += add_timestamp
        self.add_url_rule('/mark_one', 'mark_one', mark_one, methods=['POST'])
        self.add_url_rule('/bootstrap', 'bootstrap', bootstrap, methods=['GET'])
        logHandler = logging.FileHandler('app.log')
        logHandler.setLevel(logging.INFO)
        self.logger.addHandler(logHandler)
        self.logger.setLevel(logging.INFO)
        connect('eve')


def mark_one():
    raw_data = request.get_json()
    response = requests.post(current_app.config['MARKER_API_URL'] + 'mark_one', json=raw_data)
    return jsonify(json.loads(response.text))


def bootstrap():
    user = User()
    user.username='admin'
    user.password='123456'
    user.display_name='master'
    user.save()


def configure_error_handlers(server):
    @server.errorhandler(DecodeError)
    def jwt_decode_error_handler(error):
        return 'JWT decode error: '+str(error), 401

    @server.errorhandler(jwt_package.ExpiredSignatureError)
    def jwt_signature_expired_handler(error):
        return 'Signature expired. Please log in again.', 401

    @server.errorhandler(jwt_package.InvalidTokenError)
    def jwt_invalid_token_handler(error):
        return 'Invalid token. Please log in again.', 401

    @server.errorhandler(403)
    def access_forbidden(error):
        return render_template('error.html', message=str(error))
