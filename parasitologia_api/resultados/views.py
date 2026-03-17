from django.shortcuts import render
from rest_framework import status
from django.http import  HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resultados
from .serializers import ResultadosSerializer
import json

@api_view(['GET','POST','DELETE','PUT'])
def resultados_manager (request):

    #FUNÇÃO GET
    if request.method == 'GET':
        resultados_id = request.GET.get('id')

        if resultados_id:
            try:
                resultados = Resultados.objects.get(pk=resultados_id)
                serializer = ResultadosSerializer(resultados)
                return Response(serializer.data)
            except Resultados.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            resultados = Resultados.objects.all()
            serializer = ResultadosSerializer(resultados, many=True)
            return Response(serializer.data)
        
# FUNÇÃO POST
    if request.method == 'POST':

        novo_resultado = request.data
        serializer = ResultadosSerializer(data=novo_resultado)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO PUT
    if request.method == 'PUT':

        resultado_id = request.data['id']

        try:
            updated_resultado = Resultados.objects.get(pk=resultado_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ResultadosSerializer(updated_resultado, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO DELETE
    if request.method == 'DELETE':

        try:
            resultado_to_delete = Resultados.objects.get(pk=request.data['id'])
            resultado_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
