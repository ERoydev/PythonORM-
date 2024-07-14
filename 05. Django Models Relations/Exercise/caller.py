import os
from datetime import date

import django
from django.db.models import Count, Avg, F
from datetime import timedelta
from django.db.models.functions import TruncDate

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Car, Registration, Owner

def show_all_authors_with_their_books():
    all_authors = Author.objects.all().order_by('id') # Select prefetch prefetch_related
    result = []

    for author in all_authors:
        all_books = author.books.all()

        if not all_books:
            continue

        titles = ", ".join(bk.title for bk in all_books)
        result.append(f"{author.name} has written - {titles}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    all_authors = Author.objects.filter(books__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.all().order_by('-id')
    return songs


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    return avg_rating


def get_reviews_with_high_ratings(threshold: int):
    reviews = Review.objects.filter(rating__gte=threshold)
    return reviews


def get_products_with_no_reviews():
    products = Product.objects.filter(reviews__isnull=True).order_by('-name')
    return products


def delete_products_without_reviews():
    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    result = [(str(license)) for license in licenses]
    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date):
    expired_date = due_date - timedelta(days=365)
    expired_drivers = Driver.objects.filter(license__issue_date__gt=expired_date)
    return expired_drivers

def register_car_by_owner(owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    car.owner = owner
    car.registration = registration
    car.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

