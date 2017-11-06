import datetime
import json
import logging

import requests
from eve import Eve
from flask import request, jsonify, current_app
from mongoengine import connect

from Documents.patient import Patient


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
        patient.patient_name = patient_info['patientName']
        patient.dominant_hand = patient_info['dominantHand']
        patient.date_of_birth = datetime.datetime.strptime(patient_info['dateOfBirth'], current_app.config['DATE_FORMAT'])
        patient.save()
        item['patient_id'] = patient.id
        item['patient_name'] = patient_info['patientName']


def add_timestamp(response):
    for item in response['_items']:
        item['_updated_total_seconds'] = (item['_updated'] - datetime.datetime(1970, 1, 1)).total_seconds()


class ApiServer(Eve):
    def configure(self):
        self.on_insert_testdata += on_insert_testdata_callback
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

