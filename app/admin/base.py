#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.mongoengine import ModelView
import flask_login as login
from flask_babelex import lazy_gettext


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
    def render(self, template, **kwargs):
        kwargs['get_text'] = self.get_text
        return super(AuthModelView, self).render(template, **kwargs)

    def get_text(self, text):
        return lazy_gettext(text)

    def is_accessible(self):
        return bootstrap_mode() or user_has_roles_temp('admin')


class MedicalAdminIndexView(AdminIndexView):
    def render(self, template, **kwargs):
        kwargs['get_text'] = self.get_text
        return super(MedicalAdminIndexView, self).render(template, **kwargs)

    def is_accessible(self):
        return bootstrap_mode() or user_has_roles_temp('admin')

    def get_text(self, text):
        return lazy_gettext(text)

    @expose('/')
    def index(self):
        return super(MedicalAdminIndexView, self).index()
