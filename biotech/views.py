from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os

def telainicial(request):
    context = {}

    # Exemplo de "banco de bactérias" carregado manualmente
    bacterias = [
        {
            "nome": "Entamoeba",
            "descricao": "Entamoeba é um gênero de amebozoários parasitas que podem causar disenteria amebiana em humanos.",
            "color": "#3b82f6"  # Azul Tailwind (blue-500)
        },
        {
            "nome": "Giardia",
            "descricao": "Giardia é um gênero de protozoários parasitas que causam giardíase. Seu ciclo de vida alterna entre trofozoíto e cisto.",
            "color": "#10b981"  # Verde Tailwind (green-500)
        }
    ]

    context["bacterias"] = bacterias

    if request.method == "POST" and request.FILES.get("file"):
        upload_file = request.FILES["file"]
        fs = FileSystemStorage(location="media/uploads/")
        filename = fs.save(upload_file.name, upload_file)
        uploaded_file_url = fs.url(filename)

        # Exemplo: aqui você chamaria sua rede neural / YOLO / modelo de análise
        resultado = "Análise concluída: Bactéria detectada - Giardia."

        context.update({
            "file_name": upload_file.name,
            "selected_image": {"url": uploaded_file_url},
            "detected_image": {"url": uploaded_file_url},  # No real, substituiria pelo output processado
            "resultado": resultado
        })

    return render(request, "telainicial.html", context)
