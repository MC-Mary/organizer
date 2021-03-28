from django.db import models

TYPE_OF_VACCINE = (
    (1, "Obowiązkowe"),
    (2, "Wybrane_zalecane"),
)


class Vaccine(models.Model):
    name_of_vaccine = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, default='brak opisu')
    recommended_age = models.CharField(max_length=255, default='wg tabeli')
    type = models.IntegerField(choices=TYPE_OF_VACCINE, default=1)

    def __str__(self):
        return f"{self.name_of_vaccine} / {self.get_type_display()} / {self.recommended_age}"

    def get_detail_url(self):
        return f"/vaccine/{self.id}"


GENDER = (
    ("F", "Kobieta"),
    ("M", "Mężczyzna"),
)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=90)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    vaccines = models.ManyToManyField(Vaccine, through='Vaccination')

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    def get_detail_url(self):
        return f"/person/{self.id}"


class Vaccination(models.Model):
    vaccine_id = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_of_vaccination = models.DateField()
    additional = models.TextField(null=True)


class ChildDevelopment(models.Model):
    person_full_name = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_of_entry = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    head_circuit = models.FloatField(null=True)
    additional_information = models.TextField(null=True)

    def __str__(self):
        return f"{self.person_full_name} {self.date_of_entry}"

    def get_detail_url(self):
        return f"/childdevelopment/{self.id}"


class Diet(models.Model):
    age_of_child = models.IntegerField()
    nature_feeding = models.TextField()
    artificial_feeding = models.TextField()


ALLERGENS = (
    (1, "bez laktozy"),
    (2, "bez glutenu"),
    (3, "bez orzechów"),
    (4, "bez żółtka"),
    (5, "bez żółtka"),
)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    age_of_child = models.IntegerField(default=12)
    ingredients = models.TextField(null=True)
    preparation = models.TextField()
    allergens = models.IntegerField(choices=ALLERGENS)
    favorite = models.BooleanField()


class Hospitalization(models.Model):
    person_full_name = models.ForeignKey(Person, on_delete=models.CASCADE)
    name_of_hospital = models.CharField(max_length=255)
    date_of_entry = models.DateField()
    date_of_living = models.DateField(null=True)
    reason = models.CharField(max_length=50)
    description_of_reason = models.TextField()
    treatment = models.TextField()
    recommendation = models.TextField(null=True)
    additional = models.TextField(null=True)


class MedicalClinic(models.Model):
    person_full_name = models.ForeignKey(Person, on_delete=models.CASCADE)
    name_of_clinic = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    doctor = models.CharField(max_length=255)
    date_of_visit = models.DateField()
    reason = models.CharField(max_length=50)
    description_of_reason = models.TextField()
    treatment = models.TextField()
    recommendation = models.TextField(null=True)
    additional = models.TextField(null=True)
