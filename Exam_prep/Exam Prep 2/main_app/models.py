from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from .mixins import CreationDateMixin
from .managers import ProfileManager


class Profile(CreationDateMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)]
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
        validators=[MaxLengthValidator(15)]
    )

    address = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    objects = ProfileManager()



class Product(CreationDateMixin):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(100)]
    )

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    in_stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(
        default=True
    )


class Order(CreationDateMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='ordered')

    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    is_completed = models.BooleanField(default=False)