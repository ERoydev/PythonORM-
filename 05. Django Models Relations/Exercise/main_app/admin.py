from django.contrib import admin
from .models import Car
# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # v list_display se podava obekt na vsqka kolona
    list_display = ['model', 'year','owner', 'car_details']

    @staticmethod
    def car_details(car):
        try:
            owner = car.owner.name
        except AttributeError:
            owner = 'No owner'

        try:
            registration = car.registration.registration_number
        except AttributeError:
            registration = 'No registration number'

        return f"Owner: {owner}, Registration: {registration}"

    car_details.short_description = 'Car Details'
