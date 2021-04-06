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
    def get(self, request):
        return render(request, 'base.html')


class LoginView(View):
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
        logout(request)
        return redirect(reverse('base'))


class RegisterView(View):
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
    def get(self, request, id):
        person_detail = Person.objects.get(id=id)
        person_age_in_days = (datetime.now().date() - person_detail.date_of_birth).days
        person_age_in_weeks = person_age_in_days // 7
        person_age_in_months = int(person_age_in_weeks // 4.33)
        person_age_in_years = round((person_age_in_weeks / 52), 1)

        recommended_diet = Diet.objects.all()
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
               'recommended_diet': recommended_diet,
               'diet_for_person_age_in_months': diet_for_person_age_in_months}
        return render(request, 'detail_person_view.html', ctx)


class DeletePerson(LoginRequiredMixin, View):
    def get(self, request, id):
        person_id = Person.objects.get(id=id)
        person_id.delete()
        return redirect(reverse('add_person'))


class UpdatePerson(LoginRequiredMixin, View):
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
    def get(self, request, person_id, vaccine_id):
        vaccination_detail = Vaccination.objects.get(person_id=person_id, vaccine_id=vaccine_id)
        vaccination_detail.delete()
        return redirect(reverse('add_person'))


class DetailVaccination(LoginRequiredMixin, View):
    def get(self, request, person_id, vaccine_id):
        vaccine_detail = Vaccine.objects.get(id=vaccine_id)
        person_detail = Person.objects.get(id=person_id)
        vaccination_detail = Vaccination.objects.get(vaccine_id=vaccine_id, person_id=person_id)
        ctx = {'object': vaccine_detail, 'person_detail': person_detail,
               'vaccination_detail': vaccination_detail}
        return render(request, 'detail_vaccination_view.html', ctx)


class DetailVaccine(View):
    def get(self, request, id):
        vaccine_detail = Vaccine.objects.get(id=id)
        child_details = self.request.GET.get('person')
        ctx = {'object': vaccine_detail, 'child_details': child_details}
        return render(request, 'detail_vaccine_view.html', ctx)


class AddChildDevelopment(LoginRequiredMixin, View):
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


class DeleteChildDevelopment(LoginRequiredMixin, View):
    def get(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)
        child_development_detail.delete()
        return redirect(reverse('add_person'))


class UpdateChildDevelopment(LoginRequiredMixin, View):
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


# class UpdateChildDevelopment(LoginRequiredMixin, View):
#     def get(self, request, id):
#         child_development_detail = ChildDevelopment.objects.get(pk=id)
#         form = ChildDevelopmentForm(instance=child_development_detail)
#         return render(request, 'object_update_view.html', {'update_form': form})
#
#     def post(self, request, id):
#         child_development_detail = ChildDevelopment.objects.get(pk=id)
#         form = ChildDevelopmentForm(request.POST, instance=child_development_detail)
#
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('add_person'))
