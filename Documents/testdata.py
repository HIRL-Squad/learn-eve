from mongoengine import DynamicDocument, StringField, DictField


class Testdata(DynamicDocument):
    patient_name = StringField()
    patient_id = StringField()