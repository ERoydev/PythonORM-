import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location


def create_pet(name: str, species: str):
    new_pet = Pet(name=name, species=species)
    new_pet.save()
    return f'{name} is a very cute {species}!'


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    new_artifact = Artifact(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    new_artifact.save()
    return f'The artifact {name} is {age} years old!'


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


# def create_locations():
#     LOCATIONS = [
#         ("Sofia", "Sofia Region", 1329000, "The capital of Bulgaria and the largest city in the country", False),
#         ("Plovdiv", "Plovdiv Region", 346942, "The second-largest city in Bulgaria with a rich historical heritage", False),
#         ("Varna", "Varna Region", 330486, "A city known for its sea breeze and beautiful beaches on the Black Sea", False)
#     ]
#     for locat in LOCATIONS:
#         # new_location = Location(*locat)
#         new_location = Location(name=locat[0], region=locat[1], population=locat[2], description=locat[3], is_capital=locat[4])
#         new_location.save()
#

def show_all_locations():
    all_locations = Location.objects.all()
    result = []

    for location in sorted(all_locations, key=lambda x: -x.id):
        message = f'{location.name} has a population of {location.population}!'
        result.append(message)

    return '\n'.join(result)


def new_capital():
    curr_location = Location.objects.first()
    curr_location.is_capital = True
    curr_location.save()


def get_capitals():
    all_capitals = Location.objects.filter(is_capital=True)

    result = all_capitals.values('name')
    return result


def delete_first_location():
    Location.objects.first().delete()

# Create queries within functions
# 1va zadacha ------------------
# print(create_pet('Buddy', 'Dog'))

# 2ra zadacha ------------------
# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objcts.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

# 3ta zadacha ------------------
# print(show_all_locations())
# print(show_all_locations())
# print(new_capital())
# print(get_capitals())
#
