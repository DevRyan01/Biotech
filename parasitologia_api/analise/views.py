from django.shortcuts import render
from rest_framework import status
from django.http import  HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Analise
from .serializers import AnaliseSerializer
import json

@api_view(['GET','POST','DELETE','PUT'])
def analise_manager (request):

    #FUNÇÃO GET
    if request.method == 'GET':
        analise_id = request.GET.get('id')

        if analise_id:
            try:
                analise = Analise.objects.get(pk=analise_id)
                serializer = AnaliseSerializer(analise)
                return Response(serializer.data)
            except Analise.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            analise = Analise.objects.all()
            serializer = AnaliseSerializer(analise, many=True)
            return Response(serializer.data)
        
# FUNÇÃO POST
    if request.method == 'POST':

        nova_analise = request.data
        serializer = AnaliseSerializer(data=nova_analise)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO PUT
    if request.method == 'PUT':

        analise_id = request.data['id']

        try:
            updated_analise = Analise.objects.get(pk=analise_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AnaliseSerializer(updated_analise, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO DELETE
    if request.method == 'DELETE':

        try:
            analise_to_delete = Analise.objects.get(pk=request.data['id'])
            analise_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)




