from core.settings.base import INSTALLED_APPS, MIDDLEWARE

APPS = [
    "debug_toolbar",
    "querycount",
    "src.users",
]

ASGI_APPLICATION = "core.asgi.application"
AUTH_USER_MODEL = "users.UserModel"

INSTALLED_APPS += APPS

INTERNAL_IPS = [
    "127.0.0.1",
]  # for debug toolbar

MIDDLEWARE += [
    "querycount.middleware.QueryCountMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

QUERYCOUNT = {
    "THRESHOLDS": {"MEDIUM": 50, "HIGH": 200, "MIN_TIME_TO_LOG": 0, "MIN_QUERY_COUNT_TO_LOG": 0},
    "IGNORE_REQUEST_PATTERNS": [],
    "IGNORE_SQL_PATTERNS": [],
    "DISPLAY_DUPLICATES": None,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
}

# CHANNEL LAYERS CONF
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }

# DJANGO CACHE CONF
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/',
#         'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'}
#     }
# }


# CELERY CONF
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", 'redis://127.0.0.1:6379/0')
# CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", 'redis://127.0.0.1:6379/0')
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
# CELERY_BEAT_SCHEDULE = {
#     "printer": {
#         'task': 'main.tasks.check_spam_email',
#         'schedule': crontab(minute="*/1"),
#     }
# }
