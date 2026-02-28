from django.db import models

class AnaliseParasita(models.Model):
    nome_arquivo = models.CharField(max_length=255)
    imagem_resultado = models.ImageField(upload_to='resultados/')
    parasita_detectado = models.CharField(max_length=100)
    confianca = models.IntegerField()
    data_analise = models.DateTimeField(auto_now_add=True)
    lamina_id = models.CharField(max_length=50, blank=True, null=True) # Identificador da lâmina

    def __str__(self):
        return f"{self.parasita_detectado} - {self.data_analise.strftime('%d/%m/%Y')}"