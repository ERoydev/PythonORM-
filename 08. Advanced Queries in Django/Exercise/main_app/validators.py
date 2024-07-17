from django.core.validators import ValidationError


class RangeValueValidator:
    def __init__(self, min_value, max_value, message: str):
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    def __call__(self, value):
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(self.message)

    """
        Django needs this to be able to migrate this Validator
        He need to serialize the data in a way that he understands it
        
    """
    def deconstruct(self):
        return (
            # Here i point where this class is located at
            'main_app.validators.RangeValueValidator',
            # I specify all arguments that i receive
            [self.min_value, self.max_value]
            # If i have keywords arguments i specify them here again {'message': self.message} for example
        )