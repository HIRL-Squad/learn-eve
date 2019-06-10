from mongoengine import DynamicDocument, StringField, DateTimeField, IntField

HANDEDNESS = ['left', 'right', 'both']


EDUCATION_LEVEL = ['Primary 6 and below',
                   'Secondary 4 and below',
                   'ITE Diploma',
                   'Polytechnic Diploma',
                   'Bachelor’s Degree',
                   'Postgraduate Degree (Masters and above)']

DEMENTIA_TYPE = [
    "Vascular dementia",
    "Alzheimer’s disease",
    "Dementia from Parkinson’s disease (and similar disorders)",
    "Dementia with Lewy bodies",
    "Frontotemporal dementia (Pick's disease)",
    "Creutzfeldt-Jakob disease",
    "Huntington's disease",
    "Normal pressure hydrocephalus",
    "Wernicke-Korsakoff syndrome"
]


class Patient(DynamicDocument):
    patient_id = StringField(required=True, primary_key=True)
    dominant_hand = StringField(choices=HANDEDNESS)
    year_of_birth = IntField()
    assessment_date = DateTimeField(required=True)
    education = StringField()
    ethnicity = StringField()
    gender = StringField()
    income = StringField()
    dementia_type = StringField()
    general_note = StringField()
    chronic_diseases = StringField()
    site = StringField()
