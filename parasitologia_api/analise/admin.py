from django.contrib import admin

#importou a classe analise
from .models import Analise

# importou a classe Grupo e a Usuario
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

# exibi o campo analise
admin.site.register(Analise)

#retirou a classe grupo Grupo e a Usuario
admin.site.unregister(Group)
admin.site.unregister(User)


