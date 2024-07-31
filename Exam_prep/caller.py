import os
from datetime import timedelta, datetime, date

import django
from django.db.models import Count, Avg, Q, Max, F, Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)

    elif search_name:
        query = query_name

    elif search_nationality:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []
    for director in directors:
        result.append(f'Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}')

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.total_movies}."


def get_top_actor():
    best_actor = Actor.objects.prefetch_related('movies_main_role').annotate(
        number_movies=Count('movies_main_role'),
        average_rating=Avg('movies_main_role__rating')
    ).order_by('-number_movies', 'full_name').first()

    if not best_actor or not best_actor.number_movies:
        return ""

    movies = ', '.join([x.title for x in best_actor.movies_main_role.all() if x])
    return f"Top Actor: {best_actor.full_name}, starring in movies: {movies}, movies average rating: {round(best_actor.average_rating, 1)}"


def get_actors_by_movies_count():
    top_three = Actor.objects.annotate(
        num_participated=Count('related_actors')
    ).order_by('-num_participated', 'full_name')[:3]

    if not top_three or not top_three[0].num_participated:
        return ""

    result = []
    for actor in top_three:
        result.append(f"{actor.full_name}, participated in {actor.num_participated} movies")

    return '\n'.join(result)



def get_top_rated_awarded_movie():
    top_rated_movie = Movie.objects\
        .select_related('starring_actor')\
        .prefetch_related('actors')\
        .filter(is_awarded=True)\
        .order_by('-rating', 'title')\
        .first()

    if top_rated_movie is None:
        return ""

    starring_actor = top_rated_movie.starring_actor.full_name if top_rated_movie.starring_actor else 'N/A'
    participant_actors = top_rated_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ', '.join(participant_actors)

    result = (f"Top rated awarded movie: {top_rated_movie.title}, "
              f"rating: {round(top_rated_movie.rating, 1)}. Starring actor: {starring_actor}. "
              f"Cast: {cast}.")

    return result

def increase_rating():
    query = Q(is_classic=True) & Q(rating__lt=10.0)
    result = Movie.objects.filter(query)

    if not result:
        return "No ratings increased."

    updated_count = result.count()
    result.update(rating=F('rating') + 0.1)
    return f"Rating increased for {updated_count} movies."

