import pytest
from django.contrib.auth.models import User
from django.test import Client

from memo_for_you.models import Vaccine, Person, Vaccination, ChildDevelopment, Diet


@pytest.fixture
def client():
    """Create object client in tests database."""
    c = Client()
    return c


@pytest.fixture
def users():
    """Create 10 objects of users in test database."""
    users = []
    for x in range(10):
        u = User.objects.create(username=str(x))
        users.append(u)
    return users


@pytest.fixture
def vaccine():
    """Create 10 objects of vaccine in test database."""
    vaccine_list = []
    for x in range(10):
        v = Vaccine.objects.create(name_of_vaccine=str(x), description='brak opisu',
                                   recommended_age='dziecko', type='1')
        vaccine_list.append(v)
    return vaccine_list


@pytest.fixture
def person():
    """Create 10 objects of person in test database."""
    person_list = []
    for x in range(10):
        p = Person.objects.create(first_name=str(x), second_name=str(x), date_of_birth='2020-03-03',
                                  gender='1')
        person_list.append(p)
    return person_list


@pytest.fixture
def vaccination(vaccine, person):
    """Create 9 objects of vaccination in test database."""
    vaccination_list = []
    for x in range(9):
        vc = Vaccination.objects.create(vaccine_id=vaccine[x], person_id=person[x],
                                        date_of_vaccination='2020-03-03', additional='dodatkowe informacje')
        vaccination_list.append(vc)
    return vaccination_list


@pytest.fixture
def child_development(person):
    """Create 10 objects of child development in test database."""
    count = 1
    child_development_list = []
    for p in person:
        chd = ChildDevelopment.objects.create(person=p, date_of_entry='2020-03-20', weight='1',
                                              height='2', head_circuit='3', additional_information=count)
        count += 1
        child_development_list.append(chd)
    return child_development_list


@pytest.fixture
def diet():
    """Create 10 objects of diet in test database."""
    diet_list = []
    for x in range(10):
        d = Diet.objects.create(age_of_child=x, nature_feeding=str(x), artificial_feeding='No')
        diet_list.append(d)
    return diet_list
