
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator


# Create your models here.
from main_app.managers import DirectorManager
# To remove repeating

class PersonalInfoMixin(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2), MaxLengthValidator(120)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown',
        validators=[MaxLengthValidator(50)]
    )

    class Meta:
        abstract = True


class Director(PersonalInfoMixin):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    objects = DirectorManager()

class Actor(PersonalInfoMixin):
    is_awarded = models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5), MaxLengthValidator(150)]
    )

    release_date = models.DateField()
    storyline = models.TextField(
        null=True,
        blank=True
    )

    genre = models.CharField(
        max_length=6,
        validators=[MaxLengthValidator(6)],
        default=GenreChoices.OTHER,
        choices=GenreChoices
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )

    is_classic = models.BooleanField(
        default=False
    )

    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    director = models.ForeignKey(Director, related_name='movies', on_delete=models.CASCADE)
    starring_actor = models.ForeignKey(Actor, null=True, related_name='movies_main_role', on_delete=models.SET_NULL)
    actors = models.ManyToManyField(Actor, related_name='related_actors')
