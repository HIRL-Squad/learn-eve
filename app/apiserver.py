import datetime
import json

import requests
from eve import Eve

from app import app


def on_insert_testdata_callback(items):
    for item in items:
        test = item['test']
        patient_info = test['patientInfo']
        vas_cog_block = test['vasCogBlock']
        response = requests.post(app.config['MARKER_API_URL'] + 'mark', json=vas_cog_block)
        item['result'] = json.loads(response.text)
        item['patient_id'] = patient_info['patientId']
        item['patient_name'] = patient_info['patientName']
    print(item['result'])


def add_timestamp(response):
    for item in response['_items']:
        item['_updated_total_seconds'] = (item['_updated'] - datetime.datetime(1970, 1, 1)).total_seconds()


class ApiServer(Eve):
    def configure(self):
        self.on_insert_testdata += on_insert_testdata_callback
        self.on_fetched_resource_testlist += add_timestamp


@app.route('/data_migration')
def data_migration():
    pass
