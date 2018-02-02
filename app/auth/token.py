from eve.auth import TokenAuth
from flask_jwt import JWT
import jwt as jwt_package
from jwt import DecodeError
from werkzeug.security import safe_str_cmp
from flask import current_app
from app.user.models import User


def authenticate(username, password):
    user = User.objects(username=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.objects(id=user_id).first()


jwt = JWT(app=None, authentication_handler=authenticate, identity_handler=identity)


def validate_token(token):
    try:
        token_body = token.split(" ")[1]
    except IndexError:
        raise DecodeError('Bearer token malformed.')

    payload = jwt_package.decode(token_body, current_app.config.get('SECRET_KEY'))
    return payload['identity']


class JwtAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        return validate_token(token)
