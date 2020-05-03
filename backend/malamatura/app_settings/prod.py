from .base import *
from .utils import read_variable, get_variable

ALLOWED_HOSTS = ['*']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # 'ENGINE': 'django.db.backends.mysql',
        'NAME': get_variable('POSTGRES_DBNAME', 'malamatura'),
        'USER': get_variable('POSTGRES_USER', 'malamatura'),
        'PASSWORD': get_variable('POSTGRES_PASSWORD', 'malamatura'),
        'HOST': get_variable('POSTGRES_HOST', 'malamaturadb'),
        'PORT': get_variable('POSTGRES_PORT', ''),
    }
}

# email app_settings
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'malamatura@gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SECRET_KEY = read_variable('/private/secrets', 'SECRET_KEY') or get_variable('SECRET_KEY', 'unknown')
EMAIL_HOST_PASSWORD = read_variable('/private/secrets', 'EMAIL_HOST_PASSWORD') or get_variable('EMAIL_HOST_PASSWORD', 'unknown')

ALLOW_REPEATED_TESTS = get_variable('ALLOW_REPEATED_TESTS', True)
