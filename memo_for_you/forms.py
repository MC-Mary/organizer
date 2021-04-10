from django import forms
from django.core.exceptions import ValidationError

from memo_for_you.models import GENDER, Vaccine, Person
from memo_for_you.validators import check_length, check_weight, check_height


class LoginForm(forms.Form):
    """Builds a form for the login model"""
    username = forms.CharField(label="Podaj login")
    password = forms.CharField(label="Podaj hasło", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """
    Builds a form for the registration model.
    ...
    :raise: information about error, it appear if password1 and password2 are not the same.
    """
    username = forms.CharField(label="Podaj login", widget=forms.TextInput(attrs={"autocomplete": "off"}))
    password1 = forms.CharField(label="Podaj haslo", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError("Hasło drugi raz zostało źle wpisane")


class PersonForm(forms.Form):
    """Builds a form for the Person model"""
    first_name = forms.CharField(label="Podaj imię", validators=[check_length])
    second_name = forms.CharField(label="Podaj nazwisko", validators=[check_length])
    date_of_birth = forms.DateField(label="Podaj datę urodzenia dziecka", help_text="RRRR-MM-DD")
    gender = forms.ChoiceField(label='Podaj płeć dziecka', choices=GENDER)


class VaccinationForm(forms.Form):
    """Builds a form for the Vaccination model"""
    vaccine_id = forms.ModelChoiceField(label="Wybierz szczepienie", queryset=Vaccine.objects.all(),
                                        widget=forms.Select)
    person_id = forms.ModelChoiceField(label="Wybierz osobę", queryset=Person.objects.all(),
                                       widget=forms.Select)
    date_of_vaccination = forms.DateField(label="Podaj datę szzczepienia", help_text="RRRR-MM-DD")
    additional = forms.CharField(label="Informacje dodatkowe", widget=forms.Textarea)


class ChildDevelopmentForm(forms.Form):
    """Builds a form for the Child Development model"""
    person = forms.ModelChoiceField(label="Wybierz dziecko", queryset=Person.objects.all(),
                                    widget=forms.Select)
    date_of_entry = forms.DateField(label="Wpisz datę pomiaru", help_text="RRRR-MM-DD")
    weight = forms.FloatField(label="Waga dziecka", help_text="Waga w kg", validators=[check_weight])
    height = forms.FloatField(label="Wzrost dziecka", help_text="Wzrost w cm", validators=[check_height])
    head_circuit = forms.FloatField(label="Obwód głowy dziecka", help_text="Obwód głowy w cm")
    additional_information = forms.CharField(label="Informacje dodatkowe", widget=forms.Textarea)
