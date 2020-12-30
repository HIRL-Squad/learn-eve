from mongoengine import DynamicDocument, StringField, DateTimeField, IntField, BooleanField

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
    setting_of_assessment = StringField()
    level_of_education = StringField()
    assessment_date = DateTimeField()
    assessment_calendar = IntField()
    date_of_birth = DateTimeField()
    gender = StringField()
    ethnicity = StringField()
    dominant_hand = StringField(choices=HANDEDNESS)
    annual_income = StringField()
    option_of_money = StringField()
    site = StringField()
    note = StringField()
