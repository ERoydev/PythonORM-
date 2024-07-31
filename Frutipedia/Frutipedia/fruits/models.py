from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_name
# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
            validate_name
            ]
    )

    image_url = models.URLField()
    description = models.TextField()
    nutrition = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
