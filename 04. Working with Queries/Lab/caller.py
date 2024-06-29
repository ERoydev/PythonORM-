import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review
from django.db.models import F


def find_books_by_genre_and_language(book_genre, book_language):
    founded_books = Book.objects.filter(genre=book_genre, language=book_language)
    return founded_books


def find_authors_nationalities():
    all_authors = Author.objects.exclude(nationality__isnull=True)
    return '\n'.join([str(author) + f' is {author.nationality}' for author in all_authors])


def order_books_by_year():
    books = Book.objects.all().order_by('publication_year', 'title')
    result = [f'{book.publication_year} year: {book.title} by {book.author}' for book in books]
    return '\n'.join(result)


def delete_review_by_id(review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return f'Review by {review.reviewer_name} was deleted'


def filter_authors_by_nationalities(nationality):
    authors = Author.objects.filter(nationality=nationality).order_by('first_name', 'last_name')
    result = []
    for author in authors:
        if author.biography:
            result.append(author.biography)

        else:
            result.append(str(author))

    return '\n'.join(result)


def filter_authors_by_birth_year(year1, year2):
    authors = Author.objects.filter(birth_date__iso_year__range=(year1, year2)).order_by('-birth_date')
    result = [f'{author.birth_date}: {author.first_name} {author.last_name}' for author in authors]
    return '\n'.join(result)


def change_reviewer_name(reviewer_name, new_name):
    reviewers = Review.objects.filter(reviewer_name=reviewer_name).update(reviewer_name=new_name)
    return Review.objects.all()

