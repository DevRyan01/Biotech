from django.db import models
from amostras.models import Amostras


class Analise(models.Model):
    STATUS = [('PEND','Pendente'),('CONCL','Concluida'),('CANC','Cancelada')]
    status = models.CharField(max_length=5,choices=STATUS,default='PEND')
    inicializada_em =models.DateTimeField(null=True, blank= True)
    finalizada_em = models.DateTimeField(null=True,blank=True)
    amostra = models.OneToOneField(Amostras,on_delete=models.CASCADE,related_name='analise')

    def __str__(self):
        return f'Status: {self.status}'
