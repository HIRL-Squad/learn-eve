import flask_admin as admin
from app.admin.base import MedicalAdminIndexView
from flask_login import LoginManager
from flask_babelex import lazy_gettext

# Create login manager for flask-login
from app.user.models import User

login_manager = LoginManager()

# Create admin object
admin = admin.Admin(name=lazy_gettext('VasCog: Admin Portal'), index_view=MedicalAdminIndexView())


@login_manager.user_loader
def load_user(username):
    return User.objects(username=username).first()