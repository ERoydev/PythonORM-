from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator


class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(validators=[MinValueValidator(20), MaxLengthValidator(20)])
    gender = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    email = models.EmailField()
    salary = models.DecimalField(max_digits=6, decimal_places=2, default=800)
    description = models.CharField(max_length=50, null=True, blank=False)
    childrens = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)