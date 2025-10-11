# urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Importe as funções de view diretamente. Assumimos que 'views' se refere ao seu arquivo views.py
from biotech import views 



urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Rota principal: usa a função 'analises' para a página de upload/resultados
    path('', views.analises, name='analises'), 
    
    # 2. Rota para o Dashboard: usa o nome 'dashboard' (como em base.html)
    path('dashboard/', views.dashboard_list, name='dashboard'),
    
    # NOTA: A rota 'analises/<int:analise_id>/' foi removida,
    # pois a lógica de upload/visualização foi consolidada na rota raiz '/'

]

# ... (configurações DEBUG/static/media)
if settings.DEBUG:
    # Garante que arquivos de mídia (uploads) e estáticos (css, js) sejam servidos em desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Certifique-se de que STATIC_ROOT está configurado no settings.py se usar este bloco
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)