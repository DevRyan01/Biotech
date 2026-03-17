from django.shortcuts import render
from rest_framework import status
from django.http import  HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Amostras
from .serializers import AmostraSerializer
import json

@api_view(['GET','POST','DELETE','PUT'])
def amostras_manager (request):

    #FUNÇÃO GET
    if request.method == 'GET':
        amostras_id = request.GET.get('id')

        if amostras_id:
            try:
                amostras = Amostras.objects.get(pk=amostras_id)
                serializer = AmostraSerializer(amostras)
                return Response(serializer.data)
            except Amostras.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            amostras = Amostras.objects.all()
            serializer = AmostraSerializer(amostras, many=True)
            return Response(serializer.data)
        
# FUNÇÃO POST
    if request.method == 'POST':

        nova_amostra = request.data
        serializer = AmostraSerializer(data=nova_amostra)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO PUT
    if request.method == 'PUT':

        amostras_id = request.data['id']

        try:
            updated_amostras = Amostras.objects.get(pk=amostras_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AmostraSerializer(updated_amostras, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO DELETE
    if request.method == 'DELETE':

        try:
            amostras_to_delete = Amostras.objects.get(pk=request.data['id'])
            amostras_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



        #amostras = Amostras.objects.all()
      #  serializer = AmostraSerializer(amostras, many=True)
        #return Response(serializer.data)
    #return Response(status=status.HTTP_404_NOT_REQUEST)

#@api_view(['GET'])
#def get_by_nome(request, nome):

 #   try:
  #      amostras = Amostras.objects.get(paciente=nome)
   # except :
    #    return Response(status=status.HTTP_404_NOT_FOUND)
   # if request.method == 'GET':
    #    serializer = AmostraSerializer(amostras)
     #   return Response(serializer.data)

