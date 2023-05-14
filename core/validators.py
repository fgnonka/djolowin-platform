# from django.db import models
from django.core.exceptions import ValidationError

def validate_price(value):
    if value < 2000:
        raise ValidationError(
            f"{value} is not a valid price. Price must be greater than 0."
        )

