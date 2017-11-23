from mongoengine import StringField, DictField, DynamicDocument


class Testdata(DynamicDocument):
    patient_name = StringField()
    patient_id = StringField()
    test = DictField()
    result = DictField()