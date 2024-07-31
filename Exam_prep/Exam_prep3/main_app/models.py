from django.db import models
from django.core import validators
# Create your models here.

from .managers import AuthorManager


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(3)]
    )

    email = models.EmailField(
        unique=True
    )

    is_banned = models.BooleanField(
        default=False
    )

    birth_year = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1900), validators.MaxValueValidator(2005)]
    )

    website = models.URLField(
        null=True, blank=True
    )

    objects = AuthorManager()


class CategoryChoices(models.TextChoices):
    TECHNOLOGY = 'Technology', 'Technology'
    SCIENCE = 'Science', 'Science'
    EDUCATION = 'Education', 'Education'


class Article(models.Model):

    title = models.CharField(
        max_length=200,
        validators=[validators.MinLengthValidator(5)]
    )

    content = models.TextField(
        validators=[validators.MinLengthValidator(10)]
    )

    category = models.CharField(
        max_length=10,
        default=CategoryChoices.TECHNOLOGY,
        validators=[validators.MaxLengthValidator(10)],
        choices=CategoryChoices
    )

    authors = models.ManyToManyField(Author, related_name='author_articles')

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

class Review(models.Model):
    content = models.TextField(
        validators=[validators.MinLengthValidator(10)]
    )

    rating = models.FloatField(
        validators=[validators.MinValueValidator(1.0), validators.MaxValueValidator(5.0)]
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_reviews')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_reviews')

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )