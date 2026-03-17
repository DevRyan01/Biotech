from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   # path('',views.get_paciente, name= 'get_all_pacientes'),
    path('',views.paciente_manager)

    
]