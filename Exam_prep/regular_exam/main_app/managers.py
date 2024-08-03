from django.db import models
from django.db.models import Count

class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        query = self.annotate(
            num_missions=Count('missions')
        ).order_by('-num_missions', 'phone_number')

        return query