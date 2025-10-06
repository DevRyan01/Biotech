# Importa funções essenciais do Django
from django.shortcuts import render, redirect  # Para renderizar templates e redirecionar páginas
from django.core.files.storage import FileSystemStorage  # Para salvar arquivos enviados
from django.conf import settings  # Para acessar configurações do projeto (como MEDIA_ROOT)
import os  # Para manipulação de diretórios e caminhos
import random  # Para gerar valores aleatórios (simulação)
import matplotlib.pyplot as plt  # Biblioteca para geração de gráficos
import matplotlib
matplotlib.use('Agg')  # Define backend "não interativo" (necessário em servidores sem interface gráfica)
import base64  # Para converter gráficos em formato base64 e exibir em HTML
import io  # Para manipular arquivos em memória


# -------------------------------
# Dados fixos de referência
# -------------------------------
DADOS_BACTERIAS = [
    {
        "nome": "Entamoeba",  # Nome do parasita
        "descricao": "Entamoeba é um gênero de amebozoários parasitas que podem causar disenteria amebiana em humanos...",
        "color": "blue",  # Cor usada no card
        "color_code": "rgb(59, 130, 246)",  # Cor em formato RGB
        "bg_color": "rgb(239, 246, 255)",  # Cor de fundo do card
    },
    {
        "nome": "Giardia",
        "descricao": "Giardia é um genêro de protozoários parasitas anaeróbicos flagelados...",
        "color": "green",
        "color_code": "rgb(34, 197, 94)",
        "bg_color": "rgb(240, 253, 244)",
    },
]

# Lista de parasitas possíveis simulados (IA fictícia)
PARASITAS_POSSIVEIS = [
    ("Giardia", "Giardia"),
    ("Entamoeba", "Entamoeba"),
    ("Outro Parasita", "Outro")
]


# -------------------------------
# Função principal: Análises
# -------------------------------
def analises(request):
    """Função responsável por lidar com upload, pré-visualização e simulação da análise das imagens."""

    # Define diretórios para salvar arquivos enviados e temporários
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    preview_dir = os.path.join(settings.MEDIA_ROOT, "preview")
    
    # Garante que as pastas existam
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)
    
    # Configura o sistema de arquivos do Django para os diretórios criados
    fs_upload = FileSystemStorage(location=upload_dir)
    fs_preview = FileSystemStorage(location=preview_dir)

    # Cria um contexto base com informações fixas
    context = {"bacterias": DADOS_BACTERIAS}
    
    # Recupera resultados e imagens armazenadas na sessão
    resultados_analise = request.session.get('resultados_analise', [])
    images_preview = request.session.get('images_preview', [])
    
    # Adiciona ao contexto para exibição no template
    context["resultados_analise"] = resultados_analise
    context["images_preview"] = images_preview
    context["images_count"] = len(images_preview)

    # --------------------------
    # Se for uma requisição POST (usuário enviou algo)
    # --------------------------
    if request.method == "POST":
        action = request.POST.get('action')  # Identifica qual ação foi solicitada

        # =========================
        # 1️⃣ Upload de imagens (etapa 1)
        # =========================
        if request.FILES.getlist("images") and not action:
            uploaded_files = request.FILES.getlist("images")  # Recupera lista de imagens enviadas
            preview_list = []

            for upload_file in uploaded_files[:10]:  # Limita a 10 imagens
                # Salva a imagem na pasta de pré-visualização
                filename = fs_preview.save(upload_file.name, upload_file)
                file_url = settings.MEDIA_URL + "preview/" + filename
                
                # Adiciona informações no dicionário de preview
                preview_list.append({
                    "name": upload_file.name,
                    "url": file_url,
                    "path": filename
                })

            # Salva lista de imagens na sessão do usuário
            request.session['images_preview'] = preview_list
            return redirect('analises')  # Atualiza a página

        # =========================
        # 2️⃣ Limpar imagens do preview
        # =========================
        elif action == 'limpar_preview':
            if 'images_preview' in request.session:
                # Remove os arquivos temporários do diretório preview
                for img in request.session['images_preview']:
                    try:
                        file_path = os.path.join(preview_dir, img['path'])
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Erro ao remover arquivo: {e}")
                
                # Limpa a sessão
                del request.session['images_preview']
            
            return redirect('analises')

        # =========================
        # 3️⃣ Confirmar análise das imagens
        # =========================
        elif action == 'analisar':
            if 'images_preview' in request.session:
                novas_analises = []

                # Loop pelas imagens em preview
                for img_preview in request.session['images_preview']:
                    preview_path = os.path.join(preview_dir, img_preview['path'])
                    
                    if os.path.exists(preview_path):
                        # Move imagem para a pasta definitiva de uploads
                        with open(preview_path, 'rb') as f:
                            filename = fs_upload.save(img_preview['name'], f)
                        
                        # Apaga a versão em preview
                        os.remove(preview_path)
                        
                        # Gera URL definitiva
                        uploaded_file_url = settings.MEDIA_URL + "uploads/" + filename

                        # Simula uma análise com resultados aleatórios (substituir por IA real futuramente)
                        detectado, nome_curto = random.choice(PARASITAS_POSSIVEIS)
                        confianca = random.randint(80, 99)

                        # Busca dados visuais do parasita detectado
                        bacteria_detectada = next(
                            (b for b in DADOS_BACTERIAS if b["nome"] == nome_curto),
                            {"color": "yellow", "color_code": "rgb(234, 179, 8)"}
                        )

                        # Monta o resultado da análise
                        nova_analise = {
                            "nome_arquivo": img_preview['name'],
                            "url": uploaded_file_url,
                            "detectado": detectado,
                            "confianca": confianca,
                            "cor_card": bacteria_detectada["color"],
                        }
                        novas_analises.append(nova_analise)

                # Salva resultados na sessão
                resultados_analise.extend(novas_analises)
                request.session['resultados_analise'] = resultados_analise

                # Limpa o preview
                del request.session['images_preview']

                return redirect('analises')

        # =========================
        # 4️⃣ Limpar todos os resultados
        # =========================
        elif "limpar_tudo" in request.POST:
            if 'resultados_analise' in request.session:
                # Remove arquivos armazenados em uploads
                for analise in request.session['resultados_analise']:
                    try:
                        file_path = os.path.join(upload_dir, os.path.basename(analise['url']))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Erro ao remover arquivo: {e}")
                
                # Remove resultados da sessão
                del request.session['resultados_analise']

            return redirect('analises')

    # Renderiza o template de análises com os dados do contexto
    return render(request, "biotech/analises.html", context)


# ----------------------------------------------------------
# Função auxiliar: converte um gráfico Matplotlib em base64
# ----------------------------------------------------------
def gerar_grafico_base64(fig):
    """Converte um gráfico Matplotlib (fig) em uma string base64 para exibição no HTML."""
    buffer = io.BytesIO()  # Cria um buffer de memória
    fig.savefig(buffer, format='png', bbox_inches='tight')  # Salva o gráfico no buffer em formato PNG
    buffer.seek(0)  # Volta o ponteiro para o início
    image_png = buffer.getvalue()  # Lê os bytes da imagem
    buffer.close()  # Fecha o buffer
    grafico_base64 = base64.b64encode(image_png).decode('utf-8')  # Converte bytes em string base64
    return grafico_base64  # Retorna a string base64 pronta para uso no template


# -------------------------------
# Função: Dashboard
# -------------------------------
def dashboard_list(request):
    """Renderiza a página do dashboard com os gráficos de barras e pizza."""
    
    # Dados fictícios para o gráfico de barras (exemplo)
    dados_barra = [1, 8, 15, 5, 8, 12]
    labels_barra = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']

    # Recupera resultados armazenados na sessão
    resultados = request.session.get('resultados_analise', [])

    # Dicionário para contar quantas vezes cada parasita foi detectado
    contagem_parasitas = {'Giardia': 0, 'Entamoeba': 0, 'Ascaris': 0}

    # Atualiza contagem com base nas análises
    for r in resultados:
        if 'Giardia' in r['detectado']:
            contagem_parasitas['Giardia'] += 1
        elif 'Entamoeba' in r['detectado']:
            contagem_parasitas['Entamoeba'] += 1
        elif 'Ascaris' in r['detectado']:
             contagem_parasitas['Ascaris'] += 1

    # Cria listas para o gráfico de pizza
    dados_pizza = list(contagem_parasitas.values())
    labels_pizza = list(contagem_parasitas.keys())
    cores_pizza = ['#3b82f6', '#10b981', '#ef4444']  # Azul, verde e vermelho

    # Se não houver dados (nenhuma análise), usa valores de exemplo
    if sum(dados_pizza) == 0:
        dados_pizza = [25, 35, 40]
        labels_pizza = ['Giardia lamblia', 'Entamoeba histolytica', 'Ascaris lumbricoides']

    # ------------------------------
    # Criação do gráfico de barras
    # ------------------------------
    fig_barra, ax_barra = plt.subplots(figsize=(7, 4))  # Cria figura e eixos
    ax_barra.bar(labels_barra, dados_barra, color='#3b82f6')  # Cria barras azuis
    ax_barra.set_ylim(0, max(dados_barra) + 2)  # Define limite do eixo Y
    ax_barra.tick_params(axis='x', labelsize=10)  # Tamanho dos rótulos do eixo X
    ax_barra.tick_params(axis='y', labelsize=10)  # Tamanho dos rótulos do eixo Y
    ax_barra.grid(axis='y', linestyle='--', alpha=0.7)  # Grade pontilhada no eixo Y
    grafico_barra_base64 = gerar_grafico_base64(fig_barra)  # Converte o gráfico em base64
    plt.close(fig_barra)  # Libera memória

    # ------------------------------
    # Criação do gráfico de pizza
    # ------------------------------
    fig_pizza, ax_pizza = plt.subplots(figsize=(5, 5))  # Cria figura e eixos
    ax_pizza.pie(
        dados_pizza,
        labels=None,  # As legendas são mostradas no HTML, não no gráfico
        colors=cores_pizza,
        startangle=90,  # Começa do topo
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}  # Bordas brancas entre fatias
    )
    ax_pizza.axis('equal')  # Mantém formato circular
    grafico_pizza_base64 = gerar_grafico_base64(fig_pizza)  # Converte o gráfico
    plt.close(fig_pizza)  # Fecha a figura

    # Conta total de imagens carregadas (para exibir na interface)
    total_imagens_sidebar = len(request.session.get('imagens_selecionadas', []))

    # Monta o dicionário de contexto a ser enviado ao template
    contexto = {
        'grafico_barra_base64': grafico_barra_base64,  # Imagem base64 do gráfico de barras
        'grafico_pizza_base64': grafico_pizza_base64,  # Imagem base64 do gráfico de pizza
        'labels_pizza': labels_pizza,  # Nomes dos parasitas
        'cores_pizza': cores_pizza,  # Cores correspondentes
        'total_imagens': total_imagens_sidebar,  # Contador lateral
    }

    # Renderiza o template do dashboard
    return render(request, 'biotech/dashboard_list.html', contexto)
