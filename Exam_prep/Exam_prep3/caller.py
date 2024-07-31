import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Author, Article
from django.db.models import Q, F, Count, Avg


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(full_name__icontains=search_name, email__icontains=search_email)

    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name)

    elif search_email is not None:
        authors = Author.objects.filter(email__icontains=search_email)

    if not authors:
        return ""

    result = []
    ordered_authors = authors.order_by('-full_name')
    for author in ordered_authors:
        status = 'Banned' if author.is_banned else 'Not Banned'
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return '\n'.join(result)


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if top_author is None or top_author.num_of_articles == 0:
        return ""
    return f"Top Author: {top_author.full_name} with {top_author.num_of_articles} published articles."


def get_top_reviewer():
    # Tova e ediniq nachin
    # top_reviewer = Author.objects.annotate(num_of_reviews=Count('author_reviews')).first()

    # if top_reviewer is None or top_reviewer.num_of_reviews == 0:
    #     return " "

    # Tova e drugiq
    top_reviewer = Author.objects.annotate(
        num_of_reviews=Count('author_reviews')
    ).filter(
        num_of_reviews__gt=0
    ).order_by('-num_of_reviews', 'email').first()

    if not top_reviewer:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_of_reviews} published reviews."


def get_latest_article():
    latest_article = Article.objects.prefetch_related('authors', 'article_reviews').annotate(
        avg_rating=Avg('article_reviews__rating')
    ).order_by('-published_on').first()

    if latest_article is None:
        return ""

    num_reviews = latest_article.article_reviews.count()
    avg_rating = latest_article.avg_rating if latest_article.avg_rating else 0.0
    authors = ', '.join([x.full_name for x in latest_article.authors.all().order_by('full_name')])

    return f"The latest article is: {latest_article.title}. Authors: {authors}. Reviewed: {num_reviews if num_reviews else 0} times. Average Rating: {avg_rating:.2f}."


def get_top_rated_article():
    top_rated = Article.objects.annotate(
        avg_rating=Avg('article_reviews__rating'),
        num_reviews=Count('article_reviews')
    ).order_by('-avg_rating', 'title').first()

    if not top_rated or top_rated.num_reviews == 0:
        return ""

    avg_rating = top_rated.avg_rating if top_rated.avg_rating else 0
    return f"The top-rated article is: {top_rated.title}, with an average rating of {avg_rating:.2f}, reviewed {top_rated.num_reviews if top_rated.num_reviews else 0} times."


def ban_author(email=None):
    author = Author.objects.filter(email__exact=email).first()

    if author is None or email is None:
        return "No authors banned."

    num_reviews_deleted = author.author_reviews.count()

    author.is_banned = True
    author.save()
    author.author_reviews.all().delete()

    return f"Author: {author.full_name} is banned! {num_reviews_deleted} reviews deleted."
