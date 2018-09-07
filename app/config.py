from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '\\\x15\xee\x8ex\xff\x00F%h\x1f2\x1c\x8dw{X"\xf9\r\xe9\xe95P'
    SENTRY_DSN = 'https://5be8a37ac67e46e49ac06fae5f387309:60f1c341ba6f4fdda945b23abb3099b8@sentry.io/1276358'

    # JWT
    JWT_EXPIRATION_DELTA = timedelta(hours=1)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
