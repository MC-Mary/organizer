from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime

from memo_for_you.forms import PersonForm, VaccinationForm, ChildDevelopmentForm, LoginForm, RegisterForm
from memo_for_you.models import Vaccine, Person, Vaccination, ChildDevelopment
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


class DeletePerson(LoginRequiredMixin, View):
    def get(self, request, id):
        person_id = Person.objects.get(id=id)
        person_id.delete()
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


class AddChildDevelopment(LoginRequiredMixin, View):
    def get(self, request):
        form = ChildDevelopmentForm()
        child_development = ChildDevelopment.objects.all().order_by('person_full_name', 'date_of_entry')
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


class DetailPerson(LoginRequiredMixin, View):
    def get(self, request, id):
        person_detail = Person.objects.get(id=id)
        person_age = (datetime.now().date() - person_detail.date_of_birth)
        child_development_detail = list(ChildDevelopment.objects.filter(
            person_full_name__first_name__icontains=person_detail.first_name,
            person_full_name__second_name__icontains=person_detail.second_name).order_by('date_of_entry'))
        if child_development_detail:
            last_child_development_detail = child_development_detail[-1]
        else:
            last_child_development_detail = None

        ctx = {'person_detail': person_detail, 'child_development_detail': child_development_detail,
               'last_child_development_detail': last_child_development_detail, 'person_age': person_age}
        return render(request, 'detail_person_view.html', ctx)


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
        prev = self.request.GET.get('prev')
        # if not prev.startswith("/vaccination/"):
        #     prev = None
        ctx = {'object': vaccine_detail, 'prev': prev,
               'link': '*** W przyszłosci można dodać linki/odnośniki do literatury '
                       'medycznej na temat wybranej szczepionki ***'}
        return render(request, 'detail_vaccine_view.html', ctx)


class DetailChildDevelopment(LoginRequiredMixin, View):
    def get(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)
        ctx = {'object': child_development_detail,
               'link': '*** W przyszłosci można przedstawić pojedyńcze wyniki na siatce centylowej ***'}
        return render(request, 'detail_child_development_view.html', ctx)


class DeleteChildDevelopment(LoginRequiredMixin, View):
    def get(self, request, id):
        child_development_detail = ChildDevelopment.objects.get(id=id)
        child_development_detail.delete()
        return redirect(reverse('add_person'))


# class EditChildDevelopment(LoginRequiredMixin, UpdateView):
#
#     form_class = ChildDevelopmentForm
#     template_name = 'edit_child_development_view.html'
#     def get_success_url(self):
#         return self.object.person_full_name.get_detail_url()
