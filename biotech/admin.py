from django.contrib import admin
from .models import AnaliseParasita

@admin.register(AnaliseParasita)
class AnaliseParasitaAdmin(admin.ModelAdmin):
    # Isso define quais colunas você verá na tabela do Admin
    list_display = ('id', 'parasita_detectado', 'confianca', 'data_analise')
    # Adiciona filtros na lateral direita
    list_filter = ('parasita_detectado', 'data_analise')
    # Permite pesquisar pelo nome do parasita
    search_fields = ('parasita_detectado',)