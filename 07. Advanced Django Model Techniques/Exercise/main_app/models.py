from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator
from .validators import validate_name
from django.contrib.postgres.search import SearchVectorField

class Customer(models.Model):
    name = models.CharField(max_length=100,
                            validators=[validate_name]
    )

    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message="Age must be greater than or equal to 18")]
    )

    email = models.EmailField(
        error_messages={'invalid': 'Enter a valid email address'}
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+359\d{9}$',
                message="Phone number must start with '+359' followed by 9 digits"
            )
        ]
    )

    website_url = models.URLField(
        error_messages={'invalid': 'Enter a valid URL'}
    )


class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'title']
        abstract = True


class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5, message="Author must be at least 5 characters long")]
    )

    isbn = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(6, message="ISBN must be at least 6 characters long")],
        unique=True
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'


class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(8, message="Director must be at least 8 characters long")]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(9, message="Artist must be at least 9 characters long")]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        return self.price * Decimal(0.08)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * 2

    def format_product_name(self):
        return f'Product: {self.name}'


class DiscountedProduct(Product):
    def calculate_price_without_discount(self):
        return self.price * Decimal(1.20)

    def calculate_tax(self):
        return self.price * Decimal(0.05)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(1.5)

    def format_product_name(self):
        return f"Discounted Product: {self.name}"

    class Meta:
        proxy = True


class RechargeEnergyMixin:
    def recharge_energy(self, amount: int):
        self.energy = min(self.energy + amount, 100)

    class Meta:
        abstract = True


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()


# class SpiderHero(Hero):
#     class Meta:
#         proxy = True
#
#     def swing_from_buildings(self):
#         if self.energy < 80:
#             return f"{self.name} as Spider Hero is out of web shooter fluid"
#
#         self.energy -= 80
#         self.energy = max(self.energy, 1)
#         self.save()
#         return f"{self.name} as Spider Hero swings from buildings using web shooters"
#
#
#
# class FlashHero(Hero):
#     class Meta:
#         proxy = True
#
#     def run_at_super_speed(self):
#         if self.energy < 65:
#             return f"{self.name} as Flash Hero needs to recharge the speed force"
#
#         self.energy -= 65
#         self.energy = max(self.energy, 1)
#         self.save()
#         return f"{self.name} as Flash Hero runs at lightning speed, saving the day"


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['search_vector'])
        ]