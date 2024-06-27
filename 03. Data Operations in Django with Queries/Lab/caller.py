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

    # Tova e ediniqt po baven nachin
    # for student in NEW_STUDENTS:
    #     new_student = Student(*student)
    #     new_student.save()

    # Taka s comprehension postigam opimizaciq
    Student.objects.bulk_create([Student(*stud) for stud in NEW_STUDENTS])



def get_students_info():
    all_students = Student.objects.all()
    message = []
    for student in all_students:
        message.append(f'Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}')

    return '\n'.join(message)


def update_students_emails():
    all_students = Student.objects.all()

    for student in all_students:
        student.email = student.email.replace(student.email.split('@')[1], 'uni-students.com')
    # Vmesto da pisha .save() na vsqka iteraciq taka prashtam zaqvkata za create na edin put
    Student.objects.bulk_update(all_students, ['email'])


def truncate_students():
    Student.objects.all().delete()

# Run and print your queries

# add_students()

# print(get_students_info())

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

truncate_students()
print(Student.objects.all())
print(f"Number of students: {Student.objects.count()}")

