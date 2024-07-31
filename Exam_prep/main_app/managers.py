from django.db import models
from django.db.models import Count


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        all_directors = self.annotate(
            total_movies=Count('movies')
        ).order_by('-total_movies', 'full_name')
        return all_directors

