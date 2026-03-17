from django.db import models
from analise.models import Analise
from paciente.models import Paciente

class Resultados(models.Model):
    RESULTADO = [('HELMINTO','Helminto'),('PROTOZOÁRIO','Protozoário'),('GIARDIA','Giardia')]
    resultado_do_exame = models.CharField(max_length=11,choices=RESULTADO)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.resultado_do_exame}"