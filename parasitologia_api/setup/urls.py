
from django.contrib import admin
from django.urls import path, include
from amostras.views import Amostras
from analise.views import Analise
from paciente.views  import Paciente
from resultados.views import Resultados

urlpatterns = [
    path('admin/', admin.site.urls),
    path('amostras/', include('amostras.urls'), name='amostras_urls'),
    path('analise/', include('analise.urls'), name='analise_urls'),
    path('paciente/', include('paciente.urls'), name= 'paciente.urls'),
    path('resultados/', include('resultados.urls'), name= 'resultados.urls')
    ]
