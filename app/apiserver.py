import datetime
import json
import logging

import requests
from eve import Eve
from flask import request, jsonify, current_app
from mongoengine import connect

from Documents.patient import Patient
from Documents.testdata import Testdata
from app.helper.dataprocessing import load_patient_info


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


def on_inserted_humancorrection_callback(items):
    for item in items:
        test_id = item['test_id']
        corrections = item['corrections']

        testdata = Testdata.objects(id=test_id).first()
        if testdata is None:
            raise FileNotFoundError("testdata with id {0} cannot be found in the database".format(test_id))
        for i in corrections:
            correctness = corrections[i] == testdata.test['vasCogBlock'][i]['vasQues']
            testdata.result[i] = str(correctness)
        testdata.save()


def add_timestamp(response):
    for item in response['_items']:
        item['_updated_total_seconds'] = (item['updated_at'] - datetime.datetime(1970, 1, 1)).total_seconds()


class ApiServer(Eve):
    def configure(self):
        self.on_insert_testdata += on_insert_testdata_callback
        self.on_inserted_humancorrection += on_inserted_humancorrection_callback
        self.on_fetched_resource_testlist += add_timestamp
        self.add_url_rule('/mark_one', 'mark_one', mark_one, methods=['POST'])
        logHandler = logging.FileHandler('app.log')
        logHandler.setLevel(logging.INFO)
        self.logger.addHandler(logHandler)
        self.logger.setLevel(logging.INFO)
        connect('eve')


def mark_one():
    raw_data = request.get_json()
    response = requests.post(current_app.config['MARKER_API_URL'] + 'mark_one', json=raw_data)
    return jsonify(json.loads(response.text))
