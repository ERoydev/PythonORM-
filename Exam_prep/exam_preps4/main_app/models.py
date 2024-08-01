from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from .mixins import PersonalInformationMixin, Information
from .managers import DirectorManager


class Director(PersonalInformationMixin):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    objects = DirectorManager()


class Actor(PersonalInformationMixin, Information):
    pass


class MovieChoices(models.TextChoices):
    ACTION = 'Action', 'Action'
    COMEDY = 'Comedy', 'Comedy'
    DRAMA = 'Drama', 'Drama',
    OTHER = 'Other', 'Other'


class Movie(Information):
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True
    )

    genre = models.CharField(
        max_length=6,
        choices=MovieChoices,
        default=MovieChoices.OTHER
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0
    )

    is_classic = models.BooleanField(
        default=False
    )

    director = models.ForeignKey(Director,related_name='director', on_delete=models.CASCADE)
    starring_actor = models.ForeignKey(Actor, related_name='main_actor', on_delete=models.SET_NULL, null=True)
    actors = models.ManyToManyField(Actor, related_name='actors')
