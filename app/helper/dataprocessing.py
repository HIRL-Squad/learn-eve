import datetime

from flask import current_app


def load_patient_info(patient, patient_info):
    patient.patient_name = patient_info['patientName']
    patient.dominant_hand = patient_info['dominantHand']
    patient.date_of_birth = datetime.datetime.strptime(patient_info['dateOfBirth'], current_app.config['DATE_FORMAT'])
    patient.assessment_date = datetime.datetime.strptime(patient_info['assessmentDate'],
                                                         current_app.config['DATE_FORMAT'])
    patient.stroke_severity_scale = patient_info['nihss']
    patient.disability_score_mRS = patient_info['mRS']
    patient.years_of_education = patient_info['yearOfEducation']
    patient.gender = patient_info['gender']
    patient.ethnicity = patient_info['ethnicity']
    patient.onset_of_stroke = datetime.datetime.strptime(patient_info['onsetOfStroke'],
                                                         current_app.config['DATE_FORMAT'])
    patient.setting_of_assessment = patient_info['settingOfTheAssessment']
