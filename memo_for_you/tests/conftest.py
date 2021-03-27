import pytest
from django.contrib.auth.models import User
from django.test import Client

from memo_for_you.models import Vaccine, Person, Vaccination, ChildDevelopment, Diet


@pytest.fixture
def client():
    c = Client()
    return c

@pytest.fixture
def users():
    users = []
    for x in range(10):
        u = User.objects.create(username=str(x))
        users.append(u)
    return users

@pytest.fixture
def vaccine():
    vaccine_list = []
    for x in range(10):
        v = Vaccine.objects.create(name_of_vaccine=str(x), description='brak opisu',
                                   recommended_age='dziecko', type='1')
        vaccine_list.append(v)
    return vaccine_list

# 1 OPCJA:
# @pytest.fixture
# def person(vaccination):
#     person_list = []
#     for x in range(10):
#         p = Person.objects.create(first_name=str(x), second_name=str(x), date_of_birth='2020-03-03',
#                                   gender='1', vaccines=vaccination[x])
#         person_list.append(p)
#     return person_list

# 3 OPCJA:
# @pytest.fixture
# def person(vaccine):
#     count = 1
#     person_list = []
#     for v in vaccine:
#         p = Person.objects.create(first_name=str(count), second_name=str(count+1), date_of_birth='2020-03-03', gender='1')
#         p.vaccines.set(v)
#         count += 1
#         person_list.append(p)
#     return person_list

# 2 OPCJA:
# W tym wypadku podkreśla się  p.vaccines.add(vaccine[x])
@pytest.fixture
def person():
    person_list = []
    for x in range(10):
        p = Person.objects.create(first_name=str(x), second_name=str(x), date_of_birth='2020-03-03', gender='1')
        person_list.append(p)
    return person_list

@pytest.fixture
def vaccination(vaccine, person):
    vaccination_list = []
    for x in range(10):
        vc = Vaccination.objects.create(vaccine_id=vaccine[x], person_id=person[x],
                                        date_of_vaccination='2020-03-03', additional='dodatkowe informacje')
        vaccination_list.append(vc)
    return vaccination_list

@pytest.fixture
def child_development(person):
    count = 1
    child_development_list = []
    for p in person:
        chd = ChildDevelopment.objects.create(person_full_name=p, date_of_entry=count, weight='1',
                                              height='2', head_circuit='3', additional_information='info')
        count += 1
        child_development_list.append(chd)
    return child_development_list

@pytest.fixture
def diet():
    diet_list = []
    for x in range(10):
        d = Diet.objects.create(age_of_child=x, nature_feeding=str(x), artificial_feeding='No')
        diet_list.append(d)
    return diet_list




