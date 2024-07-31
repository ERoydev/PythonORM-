from django.db import models
from django.db.models import Count


class TennisPlayerManager(models.Manager):

    def get_tennis_players_by_wins_count(self):
        query = self.all().annotate(
            count_wins=Count('won_match')
        ).order_by('-count_wins', 'full_name')

        return query