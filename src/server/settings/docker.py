from .base import *

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'fe_jwt.backends.FEMicroservicesBackend',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}
