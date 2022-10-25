import os

import django
import environ
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter

env = environ.Env()
env.read_env(".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.str("DJANGO_SETTINGS_MODULE"))
django.setup()

# IMPORTANT::Just HTTP for now. (We can add other protocols later.
application = ProtocolTypeRouter({"http": AsgiHandler()})
