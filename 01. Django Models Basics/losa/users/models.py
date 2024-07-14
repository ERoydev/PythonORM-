from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator


class User(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.ForeignKey('City', on_delete=models.CASCADE, default=1, related_name='users')

    def __str__(self):
        return f'User: {self.name} with age {self.age}'


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Car(models.Model):
    model = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=10)
    user = models.ManyToManyField(User, related_name='car')


class HexField(models.CharField):
    description = 'Hexadecimal field'
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        if connection.vendor == 'postgresql':
            return 'INTEGER'

    def get_prep_value(self, value):
        if value is None:
            return None
        return int(value, 16)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return format(value, 'x')
