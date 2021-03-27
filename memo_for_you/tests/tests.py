import pytest
from django.urls import reverse
from memo_for_you.models import Vaccine, Person, Vaccination, ChildDevelopment

def test_check_base(client):
    response = client.get(reverse('base'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_person(client, person, users):
    client.force_login(users[0])
    response = client.get(reverse('add_person'))
    assert response.status_code == 200
    persons_from_view = response.context['objects']
    assert persons_from_view.count() == len(person)
    for x in persons_from_view:
        assert x in person