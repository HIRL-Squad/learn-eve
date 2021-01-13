

def test_load_patient_info(test_client):
    data = {
        "patient_id": "11242365",
        "visit": "baseline",
        "current_medications": "insulin",
        "occupation": "Manager",
        "living_arrangements": "Living alone",
        "housing_type": "HDB 2-room apartment",
        "setting_of_assessment": "trial",
        "level_of_education": "Polytechnic Diploma",
        "charleston_scale": ["Dementia", "Leukemia"],
        "high_blood_pressure": 120,
        "high_cholesterol": 160,
        "diabetes_mellitus": 8,
        "assessment_date": "13/01/2021 12:00:00",
        "assessment_calendar": 11111111,
        "date_of_birth": "13/01/1988 00:00:00",
        "gender": "male",
        "ethnicity": "Chinese",
        "dominant_hand": "left",
        "annual_income": "Below 10000",
        "option_of_money": "SGD",
        "site": "Singapore",
        "sarc_f": [1, 2, 0, 1, 1],
        "mmse_score": 100,
        "moca_score": 100,
        "diagnosis": ["NCI", "MCI", "Mild Dementia"],
        "note": "This is our test patient."
    }
    from Documents.patient import Patient

    patient = Patient(patient_id=data["patient_id"])
    from app.helper.dataprocessing import load_patient_info

    load_patient_info(patient, data)
    patient.save()
    pass
