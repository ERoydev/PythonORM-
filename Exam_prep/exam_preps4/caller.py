import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie
# Create queries within functions


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    if search_name is not None and search_nationality is not None:
        directors = (Director.objects.filter(
            full_name__icontains=search_name,
            nationality__icontains=search_nationality
        ).order_by('full_name'))

    elif search_name is not None:
        directors = Director.objects.filter(
            full_name__icontains=search_name
        ).order_by('full_name')

    else:
        directors = Director.objects.filter(
            nationality__icontains=search_nationality
        ).order_by('full_name')

    if not directors:
        return ""

    result = []
    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}")

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_num}."


def get_top_actor():
    actor = Actor.objects.annotate(
        movie_num=Count('main_actor'),
        avg=Avg('main_actor__rating')
    ).order_by('-movie_num', 'full_name').first()

    if not actor or actor.movie_num == 0:
        return ""

    movies = ', '.join([x.title for x in actor.main_actor.all()])
    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, movies average rating: {actor.avg:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        movies_num=Count('actors')
    ).filter(movies_num__gt=0).order_by('-movies_num', 'full_name')[:3]

    # Tuk ili polzvam filter ili proverqvam actors[0].movies_num == 0
    if not actors:
        return ""

    result = []
    for a in actors:
        result.append(f"{a.full_name}, participated in {a.movies_num} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(
        is_awarded=True
    ).order_by('-rating').first()

    if not movie:
        return ""

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    cast = ', '.join([x.full_name for x in movie.actors.all().order_by('full_name')])
    return f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10.0
    )

    updated = movies.update(
        rating=F('rating') + 0.1
    )

    if not updated:
        return "No ratings increased."

    return f"Rating increased for {updated} movies."
