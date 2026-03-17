from django.db import models
from paciente.models import Paciente

#dados que são iseridos
class Amostras(models.Model):
    TIPO = [('SANGUE', 'Sangue'),('FEZES','Fezes'),('OUTRO','Outro')]
    tipo_do_exame = models.CharField(max_length=6,choices=TIPO)
    Paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='amostras')

    # função para mostras parametros no historico 
    def __str__(self):
        return f' Tipo do Exame: {self.tipo_do_exame}'

