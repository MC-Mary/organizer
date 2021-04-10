from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime

from memo_for_you.forms import PersonForm, VaccinationForm, ChildDevelopmentForm, LoginForm, RegisterForm
from memo_for_you.models import Vaccine, Person, Vaccination, ChildDevelopment, Diet, GENDER
from django.urls import reverse
from django.views import View


class Index(View):
    """
    Home page view
    ...
    :return: is back to base.html.
    """
    def get(self, request):
        return render(request, 'base.html')


class LoginView(View):
    """
    Login view
    ...
    :return: if user is logged in, goes to 'base.html', else stay by login view.
    """
    def get(self, request):
        form = LoginForm()
        return render(request, 'object_list_view.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next', 'base')
                return redirect(redirect_url)
            else:
                return render(request, 'object_list_view.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        """
        Logout view
        ...
        :return: if user is logged out, goes to 'base.html'.
        """
        logout(request)
        return redirect(reverse('base'))


class RegisterView(View):
    """
    Registration view
    ...
    :return: if user is register, goes to login view, else stay by registration view.
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'object_list_view.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            u = User.objects.create(username=username)
            u.set_password(password)
            u.save()
            return redirect('login')
        else:
            return render(request, 'object_list_view.html', {'form': form})


class AddPerson(LoginRequiredMixin, View):
    """
    Create new person in data base and shows list of all persons in data base.
    ...
    :return: if user is logged in, and if dates are correct, new person appear in all persons list on add_person view.
    If user is not logged out or not register, shows login view.
    """
    def get(self, request):
        form = PersonForm()
        person = Person.objects.all()
        return render(request, 'object_list_view.html', {'form': form, 'objects': person,
                                                         'ctx': 'Lista wszystkich osób w serwisie'})

    def post(self, request):
        form = PersonForm(request.POST)
        person = Person.objects.all()
        if form.is_valid():
            Person.objects.create(**form.cleaned_data)
            return redirect(reverse('add_person'))
        return render(request, 'object_list_view.html', {'form': form, 'objects': person,
                                                         'ctx': 'Lista wszystkich osób w serwisie'})


class DetailPerson(LoginRequiredMixin, View):
    """
    Shows all information about chosen person and all information, that are related with these person.
    ...
    :param: id: pk that is id of chosen person.
    :return: if user is logged in shows person view of chosen person, else shows login view.
    """
    def get(self, request, id):
        person_detail = Person.objects.get(id=id)
        person_age_in_days = (datetime.now().date() - person_detail.date_of_birth).days
        person_age_in_weeks = person_age_in_days // 7
        person_age_in_months = int(person_age_in_weeks // 4.33)
        person_age_in_years = round((person_age_in_weeks / 52), 1)

        diet_for_person_age_in_months = Diet.objects.filter(age_of_child__icontains=person_age_in_months)

        child_development_detail = list(ChildDevelopment.objects.filter(
            person__first_name__icontains=person_detail.first_name,
            person__second_name__icontains=person_detail.second_name).order_by('date_of_entry'))
        if child_development_detail:
            last_child_development_detail = child_development_detail[-1]
        else:
            last_child_development_detail = None

        ctx = {'person_detail': person_detail, 'child_development_detail': child_development_detail,
               'last_child_development_detail': last_child_development_detail,
               'person_age_in_weeks': person_age_in_weeks, 'person_age_in_days': person_age_in_days,
               'person_age_in_months': person_age_in_months, 'person_age_in_years': person_age_in_years,
               'diet_for_person_age_in_months': diet_for_person_age_in_months}
        return render(request, 'detail_person_view.html', ctx)


class DeletePerson(LoginRequiredMixin, View):
    """
    Deletes information about chosen person.
    ...
    :param: id: pk that is id of chosen person.
    :return: if user is logged in after delete shows add person view,, else shows login view.
    """
    def get(self, request, id):
        person_detail = Person.objects.get(id=id)
        return render(request, 'delete_object_view.html', {'object': person_detail})

    def post(self, request, id):
        person_detail = Person.objects.get(id=id)
        person_detail.delete()
        return redirect(reverse('add_person'))


class UpdatePerson(LoginRequiredMixin, View):
    """
    Updates and save in data base all information of chosen person from person model.
    ...
    :param: id: pk that is id of chosen person.
    :return: if user is logged in after update shows add person view, else shows login view.
    """
    def get(self, request, id):
        person_detail = Person.objects.get(id=id)
        gender_name = GENDER
        return render(request, 'update_person_view.html',
                      {'gender_name': gender_name, 'person_detail': person_detail})

    def post(self, request, id):
        person_detail = Person.objects.get(id=id)
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')

        person_detail.first_name = first_name
        person_detail.second_name = second_name
        person_detail.date_of_birth = date_of_birth
        person_detail.gender = gender
        person_detail.save()

        return redirect(reverse('add_person'))


class AddVaccination(LoginRequiredMixin, View):
    """
    Create new vaccination and shows it in list of all vaccines that are in data base.
    ...
    :return: if user is logged in, and if dates are correct, new vaccination is save in data base
    and redirect to add vaccination view.If user is not logged out or not register, shows login view.
    """
    def get(self, request):
        form = VaccinationForm()
        vaccine = Vaccine.objects.all()
        return render(request, 'object_list_view.html',
                      {'form': form, 'objects': vaccine,
                       'ctx': 'Lista wszystkich szczepionek obowiązkowych i zalecanych'})

    def post(self, request):
        form = VaccinationForm(request.POST)
        vaccine = Vaccine.objects.all()
        if form.is_valid():
            Vaccination.objects.create(**form.cleaned_data)
            return redirect('add_vaccination')
        return render(request, 'object_list_view.html',
                      {'form': form, 'objects': vaccine,
                       'ctx': 'Lista wszystkich szczepionek obowiązkowych i zalecanych'})


class DeleteVaccination(LoginRequiredMixin, View):
    """
    Deletes information about vaccination of chosen person.
    ...
    :param: person_id: pk that is id of chosen person.
    :param: vaccine_id: pk that is id of chosen vaccine.
    :return: if user is logged in after delete shows add person view, else shows login view.
    """
    def get(self, request, person_id, vaccine_id):
        vaccination_detail = Vaccination.objects.get(person_id=person_id, vaccine_id=vaccine_id)
        return render(request, 'delete_object_view.html', {'object': vaccination_detail})

    def post(self, request, person_id, vaccine_id):
        vaccination_detail = Vaccination.objects.get(person_id=person_id, vaccine_id=vaccine_id)
        vaccination_detail.delete()
        return redirect(reverse('add_person'))


class DetailVaccination(LoginRequiredMixin, View):
    """
    Shows all information about chosen vaccination of chosen person.
    ...
    :param: person_id: pk that is id of chosen person.
    :param: vaccine_id: pk that is id of chosen vaccine.
    :return: if user is logged in shows  vaccination view of chosen vaccination, else shows login view.
    """
    def get(self, request, person_id, vaccine_id):
        vaccine_detail = Vaccine.objects.get(id=vaccine_id)
        person_detail = Person.objects.get(id=person_id)
        vaccination_detail = Vaccination.objects.get(vaccine_id=vaccine_id, person_id=person_id)
        ctx = {'object': vaccine_detail, 'person_detail': person_detail,
               'vaccination_detail': vaccination_detail}
        return render(request, 'detail_vaccination_view.html', ctx)


class UpdateVaccination(LoginRequiredMixin, View):
    """
    Updates and save in data base information about chosen vaccination.
    ...
    :param: id: pk that is id of chosen child development.
    :return: if user is logged in update information about chosen vaccination, else shows login view.
    """
    def get(self, request, person_id, vaccine_id):
        vaccination_detail = Vaccination.objects.get(vaccine_id=vaccine_id, person_id=person_id)
        vaccines = Vaccine.objects.all()
        persons = Person.objects.all()
        return render(request, 'update_vaccination_view.html', {'vaccines': vaccines,
                      'vaccination_detail': vaccination_detail, 'persons': persons})


    def post(self, request, person_id, vaccine_id):
        vaccination_detail = Vaccination.objects.get(vaccine_id=vaccine_id, person_id=person_id)

        person_id = request.POST.get('person')
        vaccine_id = request.POST.get('vaccine')
        date_of_vaccination = request.POST.get('date_of_vaccination')
        additional = request.POST.get('additional')
        person_detail = Person.objects.get(id=person_id)
        vaccine_detail = Vaccine.objects.get(id=vaccine_id)

        vaccination_detail.person_id = person_detail
        vaccination_detail.vaccine_id = vaccine_detail

        vaccination_detail.date_of_vaccination = date_of_vaccination
        vaccination_detail.additional = additional
        vaccination_detail.save()
        return redirect(reverse('add_vaccination'))


class DetailVaccine(View):
    """
    Shows all information about chosen vaccine and some information, that are related with.
    ...
    :param: id: pk that is id of chosen vaccine.
    :return: shows detail vaccine view of chosen vaccine.
    """
    def get(self, request, id):
        vaccine_detail = Vaccine.objects.get(id=id)
        ctx = {'object': vaccine_detail}
        return render(request, 'detail_vaccine_view.html', ctx)


class AddChildDevelopment(LoginRequiredMixin, View):
    """
    Create new child development and shows it in list of all child developments that are in data base.
    ...
    :return: if user is logged in, and if dates are correct, new child development  is save in data base
    and redirect to add child development view.If user is not logged out or not register, shows login view.
    """
    def get(self, request):
        form = ChildDevelopmentForm()
        child_development = ChildDevelopment.objects.all().order_by('person', 'date_of_entry')
        return render(request, 'object_list_view.html', {'form': form, 'objects': child_development,
                                                         'ctx': 'Lista wszystkich wpisów'})

    def post(self, request):
        form = ChildDevelopmentForm(request.POST)
        child_development = ChildDevelopment.objects.all()
        if form.is_valid():
            ChildDevelopment.objects.create(**form.cleaned_data)
            return redirect('add_child_development')
        return render(request, 'object_list_view.html', {'form': form, 'objects': child_development,
                                                         'ctx': 'Lista wszystkich wpisów'})


class DetailChildDevelopment(LoginRequiredMixin, View):
    """
    Shows all information about chosen child development of chosen person.
    ...
    :param: id: pk that is id of chosen child development.
    :return: if user is logged in shows  detail view of chosen child development, else shows login view.
    """
    def get(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)
        gender_of_the_child = child_development_detail.person.get_gender_display()

        person_age_on_measurement_day_in_days = \
            (child_development_detail.date_of_entry - child_development_detail.person.date_of_birth).days
        person_age_on_measurement_day_in_weeks = person_age_on_measurement_day_in_days // 7
        person_age_on_measurement_day_in_months = int(person_age_on_measurement_day_in_weeks // 4.33)
        person_age_on_measurement_day_in_years = round((person_age_on_measurement_day_in_weeks / 52), 1)

        ctx = {'object': child_development_detail, 'gender_of_the_child': gender_of_the_child,
               'person_age_on_measurement_day_in_months': person_age_on_measurement_day_in_months,
               'person_age_on_measurement_day_in_days': person_age_on_measurement_day_in_days,
               'person_age_on_measurement_day_in_years': person_age_on_measurement_day_in_years}
        return render(request, 'detail_child_development_view.html', ctx)


class ChildDevelopmentList(LoginRequiredMixin, View):
    """
    Shows all information about chosen child development of chosen person.
    ...
    :param: id: pk that is id of chosen child development.
    :return: if user is logged in shows  detail view of chosen child development, else shows login view.
    """
    def get(self, request, id):
        person_detail = Person.objects.get(id=id)

        child_development_detail = list(ChildDevelopment.objects.filter(
            person__first_name__icontains=person_detail.first_name,
            person__second_name__icontains=person_detail.second_name).order_by('date_of_entry'))

        ctx = {'object': child_development_detail, 'person_detail': person_detail}
        return render(request, 'child_development_list_view.html', ctx)

class DeleteChildDevelopment(LoginRequiredMixin, View):
    """
    Deletes information about chosen child development.
    ...
    :param: id: pk that is id of chosen child development.
    :return: if user is logged in after delete shows add person view, else shows login view.
    """
    def get(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)
        return render(request, 'delete_object_view.html', {'object': child_development_detail})

    def post(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)
        child_development_detail.delete()
        return redirect(reverse('add_person'))


class UpdateChildDevelopment(LoginRequiredMixin, View):
    """
    Updates and save in data base information about chosen child development.
    ...
    :param: id: pk that is id of chosen child development.
    :return: if user is logged in redirect to add_child_development view, else shows login view.
    """
    def get(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)
        persons = Person.objects.all()
        return render(request, 'update_child_development_view.html',
                      {'child_development_detail': child_development_detail, 'persons': persons})

    def post(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)

        person_id = request.POST.get('person')
        date_of_entry = request.POST.get('date_of_entry')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        head_circuit = request.POST.get('head_circuit')
        additional_information = request.POST.get('additional_information')

        person_detail = Person.objects.get(id=person_id)

        child_development_detail.person = person_detail
        child_development_detail.date_of_entry = date_of_entry
        child_development_detail.weight = weight
        child_development_detail.height = height
        child_development_detail.head_circuit = head_circuit
        child_development_detail.additional_information = additional_information
        child_development_detail.save()
        return redirect(reverse('add_child_development'))
