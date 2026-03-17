from rest_framework import serializers
from .models import Resultados

class ResultadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultados
        fields = '__all__'
