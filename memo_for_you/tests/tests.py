import pytest
from django.urls import reverse
from memo_for_you.models import Person, ChildDevelopment, Diet, Vaccination


@pytest.mark.django_db
def test_check_base(client):
    """Test if 'base' load correctly."""
    response = client.get(reverse('base'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_person(client, person, users):
    """Test if user can create a new person and if it appear in a list of all persons."""
    client.force_login(users[0])
    response = client.get(reverse('add_person'))
    assert response.status_code == 200
    persons_from_view = response.context['objects']
    assert persons_from_view.count() == len(person)
    for x in persons_from_view:
        assert x in person
    first_name = 'imię'
    second_name = 'nazwisko'
    date_of_birth = '2020-03-03'
    gender = 'F'
    response = client.post(reverse('add_person'), {'first_name': first_name, 'second_name': second_name,
                                                   'date_of_birth': date_of_birth, 'gender': gender})
    assert response.status_code == 302
    Person.objects.get(first_name=first_name, second_name=second_name,
                       date_of_birth=date_of_birth, gender=gender)
    assert response.url == reverse('add_person')


@pytest.mark.django_db
def test_add_vaccination(client, vaccine, person, users):
    """Test if user can add a new vaccination."""
    client.force_login(users[0])
    response = client.get(reverse('add_vaccination'))
    assert response.status_code == 200
    vaccine_id = vaccine[0].pk
    person_id = person[0].pk
    date_of_vaccination = '2020-05-05'
    additional = 'additional'
    response = client.post(reverse('add_vaccination'), {'vaccine_id': vaccine_id, 'person_id': person_id,
                                                        'date_of_vaccination': date_of_vaccination,
                                                        'additional': additional})
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_child_development(client, person, child_development, users):
    """Test if user can add new measurement named child development and if appear in a lists of it."""
    client.force_login(users[0])
    response = client.get(reverse('add_child_development'))
    assert response.status_code == 200
    child_developments_from_view = response.context['objects']
    assert child_developments_from_view.count() == len(child_development)
    for x in child_developments_from_view:
        assert x in child_development
    person = person[0].pk
    date_of_entry = '2020-01-02'
    weight = '20'
    height = '109'
    head_circuit = '53'
    additional_information = 'fictional information'

    response = client.post(reverse('add_child_development'),
                           {'person': person, 'date_of_entry': date_of_entry,
                            'weight': weight, 'height': height, 'head_circuit': head_circuit,
                            'additional_information': additional_information})
    assert response.status_code == 302
    ChildDevelopment.objects.get(person=person, date_of_entry=date_of_entry, weight=weight, height=height,
                                 head_circuit=head_circuit, additional_information=additional_information)
    assert response.url == reverse('add_child_development')


@pytest.mark.django_db
def test_detail_person(client, person, vaccination, users):
    """Test if object person and all information related with it, displayed in correct way"""
    client.force_login(users[0])
    response = client.get(f'/person/{person[0].pk}/')
    assert response.status_code == 200

    person_from_view = response.context['person_detail']
    assert person_from_view == person[0]

    age_of_person_from_view = response.context['person_age_in_months']
    diet_from_view = response.context['diet_for_person_age_in_months']
    if diet_from_view:
        assert diet_from_view == Diet.objects.filter(age_of_child__icontains=age_of_person_from_view)

    child_development_from_view = response.context['last_child_development_detail']
    if child_development_from_view:
        assert child_development_from_view == ChildDevelopment.objects.get(person=person[0])


@pytest.mark.django_db
def test_detail_vaccine(client, vaccine, users):
    """Test if all information about vaccine displayed correctly."""
    client.force_login(users[0])
    response = client.get(f'/vaccine/{vaccine[0].pk}/')
    assert response.status_code == 200

    vaccine_from_view = response.context['object']
    assert vaccine_from_view == vaccine[0]


@pytest.mark.django_db
def test_detail_vaccination(client, person, vaccine, vaccination, users):
    """Test if all information about vaccination, displayed in correct way."""
    client.force_login(users[0])
    response = client.get(f'/vaccination/{person[0].pk}/{vaccine[0].pk}/')
    assert response.status_code == 200

    vaccination_from_view = response.context['vaccination_detail']
    assert vaccination_from_view == vaccination[0]


@pytest.mark.django_db
def test_detail_child_development(client, child_development, users):
    """Tests if child development with all related information displayed correctly."""
    client.force_login(users[0])
    response = client.get(f'/childdevelopment/{child_development[0].pk}/')
    assert response.status_code == 200

    child_development_from_view = response.context['object']
    assert child_development_from_view == child_development[0]

    gender_of_the_child_from_view = response.context['gender_of_the_child']
    assert gender_of_the_child_from_view == child_development[0].person.get_gender_display()


@pytest.mark.django_db
def test_delete_person(client, person, users):
    """Test if object - person can be delete"""
    client.force_login(users[0])

    response = client.get(reverse('delete_person', args=[person[0].pk]))
    assert response.status_code == 200

    delete_person = person[0]
    delete_person.delete()
    assert Person.objects.all().count() == (len(person))-1


@pytest.mark.django_db
def test_delete_vaccination(client, person, vaccine, vaccination, users):
    """Test if object - vaccination can be delete"""
    client.force_login(users[0])

    response = client.get(f'/vaccination/delete/{person[0].pk}/{vaccine[0].pk}/')
    assert response.status_code == 200

    delete_vaccination = vaccination[0]
    delete_vaccination.delete()
    assert Vaccination.objects.all().count() == (len(vaccination))-1


@pytest.mark.django_db
def test_delete_child_development(client, child_development, users):
    """Test if object - child development can be delete"""
    client.force_login(users[0])

    response = client.get(f'/childdevelopment/delete/{child_development[0].pk}/')
    assert response.status_code == 200

    delete_child_development = child_development[0]
    delete_child_development.delete()
    assert ChildDevelopment.objects.all().count() == (len(child_development))-1
