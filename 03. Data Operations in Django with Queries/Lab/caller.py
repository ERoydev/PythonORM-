import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student

def add_students():
    NEW_STUDENTS = [
        ("FC5204", "John", "Doe", "1995-05-15", "john.doe@university.com"),
        ("FE0054", "Jane", "Smith", None, "jane.smith@university.com"),
        ("FH2014", "Alice", "Johnson", "1998-02-10", "alice.johnson@university.com"),
        ("FH2015", "Bob", "Wilson", "1996-11-25", "bob.wilson@university.com")
    ]


    for student in NEW_STUDENTS:
        new_student = Student(*student)
        new_student.save()

add_students()
# Run and print your queries