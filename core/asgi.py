import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "core.settings.dev")
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  ## IMPORTANT::Just HTTP for now. (We can add other protocols later.)
})