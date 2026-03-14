import os
import io
import csv
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .models import AnaliseParasita
from ultralytics import YOLO 


# Carrega o modelo uma única vez
MODEL_PATH = os.path.join(settings.BASE_DIR, 'best.pt')
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"ERRO AO CARREGAR MODELO: {e}")
    model = None

DADOS_BACTERIAS = [
    {"nome": "Entamoeba", "color": "blue"},
    {"nome": "Giardia", "color": "green"},
    {"nome": "Cystoisospora", "color": "purple"},
    {"nome": "Toxocara", "color": "red"},
]

def analises(request):
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    preview_dir = os.path.join(settings.MEDIA_ROOT, "preview")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)
    
    fs_preview = FileSystemStorage(location=preview_dir)
    context = {
        "bacterias": DADOS_BACTERIAS,
        "images_preview": request.session.get('images_preview', []),
        "images_count": len(request.session.get('images_preview', []))
    }

    if request.method == "POST":
        action = request.POST.get('action')

        # 1. Upload para Preview
        if request.FILES.getlist("images") and not action:
            uploaded_files = request.FILES.getlist("images")
            preview_list = []
            for upload_file in uploaded_files[:10]:
                filename = fs_preview.save(upload_file.name, upload_file)
                preview_list.append({
                    "name": upload_file.name,
                    "url": settings.MEDIA_URL + "preview/" + filename,
                    "path": filename
                })
            request.session['images_preview'] = preview_list
            return redirect('analises')

        # 2. Analisar com IA e salvar no Banco
        elif action == 'analisar':
            if 'images_preview' in request.session and model:
                for img_preview in request.session['images_preview']:
                    preview_path = os.path.join(preview_dir, img_preview['path'])
                    
                    if os.path.exists(preview_path):
                        results = model(preview_path, conf=0.25)
                        r = results[0]

                        # Lógica Híbrida (OBB ou Boxes)
                        deteccoes = r.boxes if (r.boxes is not None) else r.obb
                        label_ia, conf_val = "Negativo", 0
                        
                        if deteccoes and len(deteccoes) > 0:
                            label_ia = r.names[int(deteccoes.cls[0])]
                            conf_val = int(deteccoes.conf[0] * 100)

                        # Plotar e salvar imagem
                        im_bgr = r.plot()
                        im_rgb = Image.fromarray(im_bgr[..., ::-1])
                        
                        analise = AnaliseParasita(
                            nome_arquivo=img_preview['name'],
                            parasita_detectado=label_ia,
                            confianca=conf_val
                        )

                        buffer = io.BytesIO()
                        im_rgb.save(buffer, format="JPEG")
                        nome_final = f"res_{img_preview['path']}"
                        analise.imagem_resultado.save(nome_final, ContentFile(buffer.getvalue()), save=True)
                        
                        os.remove(preview_path) # Limpa o preview
                
                del request.session['images_preview']
                return redirect('dashboard_list')

        # 3. Limpar Preview
        elif action == 'limpar_preview':
            request.session['images_preview'] = []
            return redirect('analises')

    return render(request, "biotech/analises.html", context)

def dashboard_list(request):
    queryset = AnaliseParasita.objects.all().order_by('-data_analise')

    # Filtros
    parasita = request.GET.get('parasita')
    data_inicio = request.GET.get('data_inicio')
    conf_min = request.GET.get('confianca')

    if parasita: queryset = queryset.filter(parasita_detectado__icontains=parasita)
    if data_inicio: queryset = queryset.filter(data_analise__date=data_inicio)
    if conf_min: queryset = queryset.filter(confianca__gte=conf_min)

    # Exportações
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Data', 'Parasita', 'Confiança (%)'])
        for item in queryset:
            writer.writerow([item.id, item.data_analise, item.parasita_detectado, item.confianca])
        return response

    if request.GET.get('export') == 'pdf':
        html = render_to_string('biotech/pdf_template.html', {'analises': queryset})
        response = HttpResponse(content_type='application/pdf')
        pisa.CreatePDF(html, dest=response)
        return response

    return render(request, 'biotech/dashboard_list.html', {'resultados': queryset})
