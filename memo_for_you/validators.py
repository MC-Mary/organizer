from django.core.exceptions import ValidationError


def check_length(value):
    """Checks if the length is correct, if not, it gives a comments"""
    if len(value) < 3:
        raise ValidationError("Wyraz powinien zawierać minimum 3 litery")


def check_weight(value):
    """Checks if the weight is correct, if not, it gives a comments"""
    if value < 0:
        raise ValidationError("Nieprawidłowa waga dziecka")


def check_height(value):
    """Checks if the height is correct, if not, it gives a comments"""
    if value < 0:
        raise ValidationError("Nieprawidłowy wzrost dziecka")
