from datetime import datetime

from mongoengine import StringField, DictField, DynamicDocument, DateTimeField


class Testdata(DynamicDocument):
    patient_name = StringField()
    patient_id = StringField()
    human_correction = DictField()
    test = DictField()
    result = DictField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    device_info = DictField(default=None)
