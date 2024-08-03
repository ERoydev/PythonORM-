from django.core.validators import ValidationError


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError(
            f'{value} is not a valid phone number. It must contain only digits.'
        )