from datetime import datetime
from django.core.exceptions import ValidationError


def check_length(value):
    if len(value) < 3:
        raise ValidationError("Wyraz powinien zawierać minimum 3 litery")


# def check_date_of_birth(value):
#     if value>datetime.now().date:
#         raise ValidationError("Nieprawidłowa data urodzenia - dziecko jeszcze się nie urodziło.")

def check_weight(value):
    if value < 0:
        raise ValidationError("Nieprawidłowa waga dziecka")


def check_height(value):
    if value < 0:
        raise ValidationError("Nieprawidłowy wzrost dziecka")
