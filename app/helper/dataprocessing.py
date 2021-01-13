import datetime

from flask import current_app
from mongoengine import StringField, IntField, DateTimeField, BooleanField


def cast_data_to_field_type(field, original):
    if isinstance(field,StringField):
        return original
    if isinstance(field,IntField):
        return original
    if isinstance(field,BooleanField):
        return original
    if isinstance(field,DateTimeField):
        return datetime.datetime.strptime(original, current_app.config['DATE_FORMAT'])
    return original


def load_patient_info(patient, patient_info):
    for field_name in patient_info.keys():
        if field_name in patient._fields:
            casted_data = cast_data_to_field_type(patient._fields[field_name], patient_info[field_name])
            patient[field_name] = casted_data
