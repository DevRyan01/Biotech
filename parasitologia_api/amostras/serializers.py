from rest_framework import serializers
from .models import Amostras


class AmostraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amostras
        fields ='__all__' # muda os campos que seram exibidos no json
