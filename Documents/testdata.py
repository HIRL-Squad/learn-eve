from datetime import datetime

from mongoengine import StringField, DictField, DynamicDocument, DateTimeField


class Testdata(DynamicDocument):
    patient_name = StringField()
    patient_id = StringField()
    test = DictField()
    result = DictField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self):
        self.updated_at = datetime.utcnow()
        super(Testdata, self).save()