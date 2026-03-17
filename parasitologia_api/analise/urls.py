from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.get_analise, name='get_all_analise')
    path('',views.analise_manager)
]