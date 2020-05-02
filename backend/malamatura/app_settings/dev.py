from .base import *
from .utils import get_variable

DEBUG = True

ALLOWED_HOSTS = ['localhost', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ATOMIC_REQUESTS': True,  # opseg transakcije = HTTP zahtev
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fpmh!s6dc3h_^#zuk&(qy6(r1^0!k-q%60b03ki4gg5jpmi1v&'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOW_REPEATED_TESTS = get_variable('ALLOW_REPEATED_TESTS', True)
