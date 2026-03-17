from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.amostras_manager)
   #path('', views.get_amostras, name= 'get_all_amostras'),
  # path('paciente/<str:nome>', views.get_by_nome),

]