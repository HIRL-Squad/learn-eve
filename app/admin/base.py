#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.mongoengine import ModelView
import flask_login as login


def user_has_roles_temp(*roles):
    for role in roles:
        if role in [str(role) for role in login.current_user.roles]:
            return True
    return False


def bootstrap_mode():
    from app.user.models import User
    return User.objects().count() <= 1


class AuthView(BaseView):
    def is_accessible(self):
        return bootstrap_mode() or user_has_roles_temp('admin')


class AuthModelView(ModelView):
    def is_accessible(self):
        return bootstrap_mode() or user_has_roles_temp('admin')


class MedicalAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return bootstrap_mode() or user_has_roles_temp('admin')

    @expose('/')
    def index(self):
        return super(MedicalAdminIndexView, self).index()
