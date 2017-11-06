from mongoengine import Document, StringField, DateTimeField

HANDEDNESS = ('left', 'right', 'both')


class Patient(Document):
    patient_id = StringField(required=True, primary_key=True)
    patient_name = StringField(required=True)
    dominant_hand = StringField(choices=HANDEDNESS)
    date_of_birth = DateTimeField(required=True)