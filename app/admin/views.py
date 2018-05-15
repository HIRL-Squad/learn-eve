from Documents.patient import Patient
from Documents.testdata import Testdata
from app.user.models import User, Role
from app.extensions import admin
from app.user.admin import UserView, RoleView
from Documents.admin import PatientView, TestdataView


for model in (User, Role, Patient, Testdata):
    admin.add_view(
        locals()[model.__name__ + 'View'](model)
    )