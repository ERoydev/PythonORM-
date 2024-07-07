from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
# Create your models here.


class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        age = date.today() - self.birth_date
        return age.days // 365
# Multi-table Inheritance
class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


#   Abstract Base Classes
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    class SpecialtyChoices(models.TextChoices):
        MAMMALS = 'Mammals', 'Mammals'
        BIRDS = 'Birds', 'Birds'
        REPTILES = 'Reptiles', 'Reptiles'

    specialty = models.CharField(max_length=10, choices=SpecialtyChoices)
    managed_animals = models.ManyToManyField(Animal)

    def clean(self):
        if self.specialty not in self.SpecialtyChoices:
            raise ValidationError("Specialty must be a valid choice.")


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)


# Proxy Models
class ZooDisplayAnimal(Animal):

    class Meta:
        proxy = True

    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self):
        if self.species in ['Cross River Gorilla', 'Orangutan', 'Green Turtle']:
            return f"{self.species} is at risk!"

        else:
            return f"{self.species} is not at risk."