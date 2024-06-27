import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Person, Order
from datetime import timedelta

orders = Order.objects.all()

for ord in orders:
    delivery_date = ord.order_date + timedelta(days=3)
    print(ord.order_date)
    print(delivery_date)
    print('-----------')