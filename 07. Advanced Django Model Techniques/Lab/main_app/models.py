from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Restaurant(models.Model):
    name = models.CharField(max_length=150,
                            validators=[MinLengthValidator(2, message='Name must be at least 2 characters long.'),
                                        MaxLengthValidator(100, message='Name cannot exceed 100 characters.')])

    location = models.CharField(max_length=150,
                                validators=[MinLengthValidator(2, message='Location must be at least 2 characters long.'),
                                            MaxLengthValidator(200, message="Location cannot exceed 200 characters.")])

    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[MinValueValidator(0, message="Rating must be at least 0.00."),
                                             MaxValueValidator(5, message="Rating cannot exceed 5.00.")])



def validate_categories(value):
    if value not in ('Appetizers', 'Main Course', 'Desserts'):
        raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')



class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[validate_categories])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class RestaurantReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ('reviewer_name', 'restaurant')
        abstract = True


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'
        unique_together = ['reviewer_name', 'restaurant']