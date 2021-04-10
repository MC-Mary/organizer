"""organizer_for_parents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from memo_for_you import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='base'),
    path('addperson/', views.AddPerson.as_view(), name='add_person'),
    path('addvaccination/', views.AddVaccination.as_view(), name='add_vaccination'),
    path('addchilddevelopment/', views.AddChildDevelopment.as_view(), name='add_child_development'),
    path('person/<int:id>/', views.DetailPerson.as_view(), name='person'),
    path('vaccine/<int:id>/', views.DetailVaccine.as_view(), name='vaccine'),
    path('vaccination/<int:person_id>/<int:vaccine_id>/', views.DetailVaccination.as_view(),
         name='vaccination'),
    path('childdevelopment/<int:id>/', views.DetailChildDevelopment.as_view(), name='child_development'),
    path('childdevelopmentlist/<int:id>/', views.ChildDevelopmentList.as_view(), name='child_development_list'),
    path('person/delete/<int:id>/', views.DeletePerson.as_view(), name='delete_person'),
    path('vaccination/delete/<int:person_id>/<int:vaccine_id>/', views.DeleteVaccination.as_view(),
         name='delete_vaccination'),
    path('childdevelopment/delete/<int:id>/', views.DeleteChildDevelopment.as_view(),
         name='delete_child_development'),

    path('person/update/<int:id>/', views.UpdatePerson.as_view(), name='update_person'),
    path('vaccination/update/<int:person_id>/<int:vaccine_id>/', views.UpdateVaccination.as_view(),
         name='update_vaccination'),
    path('childdevelopment/update/<int:id>/', views.UpdateChildDevelopment.as_view(),
         name='update_child_development'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
