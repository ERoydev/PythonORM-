import os
from datetime import date

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Count, Q, Avg, Sum
from main_app.models import Astronaut, Mission, Spacecraft


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts:
        return ""

    result = []
    for a in astronauts:
        result.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}")

    return '\n'.join(result) if result else ''


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or astronaut.num_missions == 0:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.num_missions} missions."


def get_top_commander():
    commander = Astronaut.objects.annotate(
        num_missions=Count('commanded_missions')
    ).order_by('-num_missions', 'phone_number').first()

    if not commander or commander.num_missions == 0:
        return "No data."

    return f"Top Commander: {commander.name} with {commander.num_missions} commanded missions."


def get_last_completed_mission():
    mission = Mission.objects.filter(
        status='Completed',
    ).annotate(
        space_walks=Sum('astronauts__spacewalks')
    ).order_by('-launch_date').first()

    if mission is None:
        return "No data."

    astronauts = [x.name for x in mission.astronauts.all().order_by('name')]
    commander_name = mission.commander.name if mission.commander else 'TBA'
    result = f"The last completed mission is: {mission.name}. Commander: {commander_name}. Astronauts: {', '.join(astronauts)}. Spacecraft: {mission.spacecraft.name}. Total spacewalks: {mission.space_walks}."
    return result


def get_most_used_spacecraft():
    spacecrafts = Spacecraft.objects.annotate(
        num_missions=Count('used_in_missions', distinct=True)
    ).filter(num_missions__gt=0).order_by('-num_missions', 'name')

    if not spacecrafts.exists():
        return "No data."

    top_spacecraft = spacecrafts.first()
    num_astronauts = Mission.objects.filter(
        spacecraft=top_spacecraft
    ).values('astronauts').count()

    result = f"The most used spacecraft is: {top_spacecraft.name}, manufactured by {top_spacecraft.manufacturer}, used in {top_spacecraft.num_missions} missions, astronauts on missions: {num_astronauts}."
    return result


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(
        used_in_missions__status='Planned',
        weight__gte=200.0
    ).distinct()

    if not spacecrafts.exists():
        return "No changes in weight."

    for spacecraft in spacecrafts:
        # potencialna greshka !!!!
        spacecraft.weight = max(spacecraft.weight - 200.0, 0.0)
        spacecraft.save()

    avg_weight = Spacecraft.objects.all().aggregate(avg_weight=Avg('weight'))['avg_weight']

    num_of_spacecrafts = spacecrafts.count()
    result = f"The weight of {num_of_spacecrafts} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"
    return result

