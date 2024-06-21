import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "losa.settings")
django.setup()

from users.models import User