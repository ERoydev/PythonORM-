import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "losa.settings")
django.setup()

from users.models import User


all_user = User.objects.all()
single_user = User.objects.get(pk=5)
filter_user = User.objects.filter(pk=10)
print(filter_user)