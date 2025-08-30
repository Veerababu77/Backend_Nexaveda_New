"""For validatings Fields."""

import re
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    """
    Validates Indian phone numbers (10 digits, starting with 6-9).
    Example: 9876543210
    """
    pattern = r'^[6-9]\d{9}$'
    if not re.match(pattern, str(value)):
        raise ValidationError("Enter a valid 10-digit number, starting with 6-9")