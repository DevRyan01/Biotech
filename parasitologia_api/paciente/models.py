from django.db import models

class Paciente(models.Model):
    paciente = models.CharField(max_length=64, null= False, blank= False)
    data_de_nascimento = models.DateField(null= True , blank= True)

    def __str__(self):
        return f'Nome do Paciente: {self.paciente} | Data de Nascimento: {self.data_de_nascimento}'
    
    