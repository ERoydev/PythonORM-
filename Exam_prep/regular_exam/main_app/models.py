from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from .managers import AstronautManager


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError(f'{value} is not a valid phone number. It must contain only digits.')


class Astronaut(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_phone_number]
    )

    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)

    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)


class Mission(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed')
    ]

    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default='Planned'
    )
    launch_date = models.DateField()
    updated_at = models.DateTimeField(
        auto_now=True
    )

    spacecraft = models.ForeignKey(Spacecraft,
        on_delete=models.CASCADE,
        related_name='used_in_missions'
    )

    astronauts = models.ManyToManyField(Astronaut, related_name='missions')
    commander = models.ForeignKey(Astronaut, null=True, on_delete=models.SET_NULL, related_name='commanded_missions')
