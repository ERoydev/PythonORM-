from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
# Create your models here.
from main_app.managers import TennisPlayerManager

class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(5)]
    )

    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(300)
        ]
    )

    is_active = models.BooleanField(
        default=True
    )

    objects = TennisPlayerManager()


class SurfaceChoices(models.TextChoices):
    NOT_SELECTED = 'Not Selected', 'Not Selected'
    CLAY = 'Clay', 'Clay'
    GRASS = 'Grass', 'Grass'
    HARD_COURT = 'Hard Court', 'Hard Court'


class Tournament(models.Model):
    name = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2)],
        unique=True
    )

    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    start_date = models.DateField()

    surface_type = models.CharField(
        choices=SurfaceChoices,
        max_length=12,
        default=SurfaceChoices.NOT_SELECTED
    )


class Match(models.Model):
    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    score = models.CharField(
        max_length=100
    )

    summary = models.TextField(
        validators=[MinLengthValidator(5)]
    )

    date_played = models.DateTimeField()

    tournament = models.ForeignKey(Tournament, related_name='all_matches', on_delete=models.CASCADE)
    players = models.ManyToManyField(TennisPlayer, related_name='players')
    winner = models.ForeignKey(TennisPlayer, related_name='won_match', on_delete=models.SET_NULL, null=True)