import os

import django
from django.db.models import Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout, BrandChoices

# 1va zad
def show_highest_rated_art():
    high_rated_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{high_rated_art.art_name} is the highest-rated art with a {high_rated_art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create(first_art, second_art)


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lte=0).delete()
# --------------------------



# 2ra zad
def show_the_most_expensive_laptop():
    laptop = Laptop.objects.order_by('-price', '-id').first()
    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"


def bulk_create_laptops(args):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    laptops = Laptop.objects.filter(brand__in=('Asus', 'Acer')).update(storage=512)


def update_to_16_GB_memory():
    laptops = Laptop.objects.filter(brand__in=('Apple', 'Dell', 'Acer')).update(memory=16)


def update_operation_systems():
    Laptop.objects.update(
        operation_sytem=Case(
            When(brand=BrandChoices.ACER, then=Value('Windows')),
            When(brand=BrandChoices.APPLE, then=Value('MacOS')),
            When(brand=BrandChoices.DELL, then=Value('Linux')),
            When(brand=BrandChoices.LENOVO, then=Value('Chrome OS'))
        )
    )


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()
# --------------------------



# 3ta zad
def bulk_create_chess_players(args):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.update(games_drawn=10)

def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')

def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title='IM')


def grand_chess_title_FM():
    ChessPlayer.objects.filtyer(rating__range=(2200, 2299)).update(title='FM')

def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title='regular player')


# --------------------------

# 4ta zad
def set_new_chefs():
    Meal.objects.update(
        chef=Case(
            When(meal_type='Breakfast', then=Value('Gordon Ramsay')),
            When(meal_type='Lunch', then=Value('Julia Child')),
            When(meal_type='Dinner', then=Value('Jamie Oliver')),
            When(meal_type='Snack', then=Value('Thomas Keller'))
        )
    )


def set_new_preparation_times():
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type='Breakfast', then=Value('10 minutes')),
            When(meal_type='Lunch', then=Value('12 minutes')),
            When(meal_type='Dinner', then=Value('15 minutes')),
            When(meal_type='Snack', then=Value('5 minutes'))
        )
    )


def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=('Breakfast', 'Dinner')).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=('Lunch', 'Snack')).update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=('Lunch', 'Snack')).delete()

# --------------------------

# 5ta zad
def show_hard_dungeons():
    hard_dungeons = Dungeon.objects.filter(difficulty='Hard').order_by('-location')
    result = [str(dun) for dun in hard_dungeons]
    return '\n'.join(result)


def bulk_create_dungeons(args):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
            When(difficulty='Easy', then=Value('The Erased Thombs')),
            When(difficulty='Medium', then=Value('The Coral Labyrinth')),
            When(difficulty='Hard', then=Value('The Lost Haunt'))
        )
    )


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty='Easy').update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty='Easy', then=Value(25)),
            When(difficulty='Medium', then=Value(50)),
            When(difficulty='Hard', then=Value(75))
        )
    )


def update_dungeon_rewards():
    Dungeon.objects.update(
        reward=Case(
            When(location__startswith="E", then=Value('New dungeon unlocked')),
            When(location__endswith="s", then=Value('Dragonheart Amulet')),
            When(boss_health=500, then=Value('1000 Gold'))
        )
    )


def set_new_locations():
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss'))
        )
    )
# --------------------------


# 6ta zad
def show_workouts():
    workouts = Workout.objects.filter(workout_type__in=('Calisthenics', 'CrossFit'))
    result = [str(workout) for workout in workouts]
    return '\n'.join(result)


def get_high_difficulty_cardio_workouts():
    workouts = Workout.objects.filter(workout_type='Cardio', difficulty='High').order_by('instructor')
    return workouts


def set_new_instructors():
    Workout.objects.update(
        instructor=Case(
            When(workout_type='Cardio', then=Value('John Smith')),
            When(workout_type='Strength', then=Value('Michael Williams')),
            When(workout_type='Yoga', then=Value('Emily Johnson')),
            When(workout_type='CrossFit', then=Value('Sarah Davis')),
            When(workout_type='Calisthenics', then=Value('Chris Heria'))
        )
    )

def set_new_duration_times():
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes'))
        )
    )

def delete_workouts():
    Workout.objects.exclude(workout_type__in=('Calisthenics', 'Strength')).delete()



Workout.objects.all().delete()
# Create two Workout instances
workout1 = Workout.objects.create(
    name="Push-Ups",
    workout_type="Calisthenics",
    duration="10 minutes",
    difficulty="Intermediate",
    calories_burned=200,
    instructor="Bob"
)

workout2 = Workout.objects.create(
    name="Running",
    workout_type="Cardio",
    duration="30 minutes",
    difficulty="High",
    calories_burned=400,
    instructor="Lilly"
)

# Run the functions
print(show_workouts())

high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
for workout in high_difficulty_cardio_workouts:
    print(f"{workout.name} by {workout.instructor}")

set_new_instructors()
for workout in Workout.objects.all():
    print(f"Instructor: {workout.instructor}")

set_new_duration_times()
for workout in Workout.objects.all():
    print(f"Duration: {workout.duration}")

# --------------------------