from rest_framework import serializers
from .models import Analise

class AnaliseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analise
        fields = '__all__'