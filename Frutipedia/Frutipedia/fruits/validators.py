from django.core.validators import ValidationError


def validate_name(value):
    if not value.isalpha():
        raise ValidationError("Fruit name should contain only letters!")