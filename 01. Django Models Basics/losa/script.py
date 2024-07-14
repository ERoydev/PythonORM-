import os
import random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "losa.settings")
django.setup()

from users.models import User, Car, City


users = User.objects.all()
cars = Car.objects.all()

for u in users:
    u.car_set.add(random.choice(cars))