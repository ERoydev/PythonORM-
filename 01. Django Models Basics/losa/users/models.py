from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator


class User(models.Model):
    class CityChoices(models.TextChoices):
        VARNA = 'VR', 'Varna'
        BURGAS = "BS", 'Burgas'
        PLOVDIV = 'PL', 'Plovdiv'
        SOFIA = 'SF', 'Sofia'

    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f'User: {self.name} with age {self.age}'
