from django.db import models
from django.db.models import Count, Q, F, Max, Min, Avg

class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price, max_price):
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self):
        popular_locations = self.values('location').annotate(
            location_count=Count('id')
        ).order_by('-location_count', 'location')[:2]

        return popular_locations


class VideoGameManager(models.Manager):

    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        result = self.annotate(
            highest=Max('rating')
        ).order_by('-highest')[0]

        return result

    def lowest_rated_game(self):
        result = self.annotate(
            lowest=Min('rating')
        ).order_by('lowest')[0]

        return result

    def average_rating(self):
        result = self.aggregate(
            avg=Avg('rating')
        )

        return round(result['avg'], 1)


