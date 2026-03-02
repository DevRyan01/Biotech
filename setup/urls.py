from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Importamos as views diretamente do seu app 'biotech'
from biotech import views 

urlpatterns = [
    # 1. Painel Administrativo do Django
    path('admin/', admin.site.urls),
    
    # 2. Página Principal (Upload e Análise em tempo real)
    # No views.py: return redirect('analises')
    path('', views.analises, name='analises'), 
    
    # 3. Dashboard e Relatórios (Lista de resultados salvos no banco)
    # No views.py: return redirect('dashboard_list')
    path('dashboard/', views.dashboard_list, name='dashboard_list'),
]

# --- CONFIGURAÇÃO DE ARQUIVOS DE MÍDIA E ESTÁTICOS ---
# Isso permite que o Django exiba as imagens que a IA salvou durante o desenvolvimento
if settings.DEBUG:
    # Serve arquivos de upload (fotos dos parasitas e resultados)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Serve arquivos estáticos (CSS, JavaScript, Imagens do sistema)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)