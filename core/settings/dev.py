from base import *

ASGI_APPLICATION = 'core.asgi.application'
AUTH_USER_MODEL = "users.UserModel"


APPS = [
    'src.Ninja.users',
    'src.educations',
    # 'src.other_apps.main',
    # 'src.chat',
    # "channels"
]

INSTALLED_APPS += APPS


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
