from django.db import models
from .managers import RealEstateListingManager, VideoGameManager
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import RangeValueValidator
# Create your models here.
from django.db.models import F, Q
from datetime import date, timedelta


class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    objects = RealEstateListingManager()


class VideoGame(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_year = models.PositiveIntegerField(
        validators=[RangeValueValidator(
            min_value=1990,
            max_value=2023,
            message='The release year must be between 1990 and 2023')]
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[RangeValueValidator(
            min_value=0.0,
            max_value=10.0,
            message='The rating must be between 0.0 and 10.0'
        )]
    )

    objects = VideoGameManager()

    def __str__(self):
        return self.title


class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)

    @classmethod
    def get_invoices_with_prefix(cls, prefix: str):
        result = cls.objects.filter(invoice_number__startswith=prefix)
        return result

    @classmethod
    def get_invoices_sorted_by_number(cls):
        return cls.objects.all().order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number: str):
        result = cls.objects.select_related('billing_info').get(invoice_number=invoice_number)
        return result

class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology, related_name='projects')

    def get_programmers_with_technologies(self):
        query = self.programmers.prefetch_related('projects')
        return query


class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, related_name='programmers')

    def get_projects_with_technologies(self):
        query = self.projects.prefetch_related('technologies_used')
        return query


class Task(models.Model):
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()

    @classmethod
    def ongoing_high_priority_tasks(cls):
        result = cls.objects.filter(
            is_completed=False,
            priority='High',
            completion_date__gt=F('creation_date')
        )
        return result

    @classmethod
    def completed_mid_priority_tasks(cls):
        result = cls.objects.filter(
            is_completed=True,
            priority='Medium'
        )
        return result

    @classmethod
    def search_tasks(cls, query: str):
        result = cls.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return result

    @classmethod
    def recent_completed_tasks(cls, days: int):
        result = cls.objects.filter(
            is_completed=True,
            completion_date__gte=F('creation_date') - timedelta(days=days)
        )
        return result



class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    @classmethod
    def get_long_and_hard_exercises(cls):
        result = cls.objects.filter(
            duration_minutes__gt=30,
            difficulty_level__gte=10
        )
        return result

    @classmethod
    def get_short_and_easy_exercises(cls):
        result = cls.objects.filter(
            duration_minutes__lt=15,
            difficulty_level__lt=5
        )
        return result

    @classmethod
    def get_exercises_within_duration(cls, min_duration: int, max_duration: int):
        result = cls.objects.filter(
            duration_minutes__range=(min_duration, max_duration)
        )
        return result

    @classmethod
    def get_exercises_with_difficulty_and_repetitions(cls, min_difficulty, min_repetitions):
        result = cls.objects.filter(
            difficulty_level__gte=min_difficulty,
            repetitions__gte=min_repetitions
        )
        return result

