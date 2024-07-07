import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import ZooKeeper, Veterinarian, Mammal

# Keep the data from the previous exercise, so you can reuse it
from main_app.models import ZooDisplayAnimal

# Keep the data from the previous exercises, so you can reuse it
