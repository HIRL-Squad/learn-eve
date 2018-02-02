from app.user.models import User, Role
from app.extensions import admin
from app.user.admin import UserView, RoleView


for model in (User, Role):
    admin.add_view(
        locals()[model.__name__ + 'View'](model)
    )