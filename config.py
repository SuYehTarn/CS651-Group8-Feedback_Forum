"""Module of app configuration"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Class of configuration"""
    # Form
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 b'\x876\xeb_\xc9<?\xb8r\xcak\r[\xa0\xf4\xfe\xdbP\xae\x17\x15S\xa5^'

    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FEEDBACK_FORUM_MAIL_SUBJECT_PREFIX = '[Feedback Forum]'
    FEEDBACK_FORUM_MAIL_SENDER = 'Feedback Forum Admin <cs651-group8@gmail.com>'
    FEEDBACK_FORUM_ADMIN = os.environ.get('FEEDBACK_FORUM_ADMIN')

    # DataBase
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Administrator
    ADMIN_NAME = os.environ.get('ADMIN_NAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    # Review Statuses
    REVIEW_STATUSES = [
        'PENDING',
        'PROCESSING',
        'CLOSED',
    ]

    @staticmethod
    def init_app(app):
        """Initialize the app with this configuration"""


class DevelopmentConfig(Config):
    """Class of configuration on developing"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    """Class of configuration on testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Class of configuration on production"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
