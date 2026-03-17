from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.resultados_manager)
    #path('',views.get_resultados, name= 'get_all_resultados'),
    ]