# from __future__ import absolute_import, unicode_literals
#
# import os
#
# import environ
# from celery import Celery
# from django.apps import apps
# from django.conf import settings
#
# env = environ.Env()
# env.read_env(".env")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.str("DJANGO_SETTINGS_MODULE"))
#
# app = Celery("core")
# app.config_from_object("django.conf:settings", namespace="CELERY")
#
# app.config_from_object(settings)
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
#
# app.conf.update(enable_utc=True, timezone="Asia/Tashkent")
