from django.shortcuts import render
from rest_framework import status
from django.http import  HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Paciente
from .serializers import PacienteSerializer
import json

@api_view(['GET', 'POST','PUT', 'DELETE'])
def paciente_manager(request):


# FUNÇÃO GET
    if request.method == 'GET':

        paciente_id = request.GET.get('id')

        if paciente_id:
            try:
                paciente = Paciente.objects.get(pk=paciente_id)
                serializer = PacienteSerializer(paciente)
                return Response(serializer.data)
            except Paciente.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            pacientes = Paciente.objects.all()
            serializer = PacienteSerializer(pacientes, many=True)
            return Response(serializer.data)


# FUNÇÃO POST
    if request.method == 'POST':

        novo_paciente = request.data
        serializer = PacienteSerializer(data=novo_paciente)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO PUT
    if request.method == 'PUT':

        paciente_id = request.data['id']

        try:
            updated_paciente = Paciente.objects.get(pk=paciente_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PacienteSerializer(updated_paciente, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FUNÇÃO DELETE
    if request.method == 'DELETE':

        try:
            paciente_to_delete = Paciente.objects.get(pk=request.data['id'])
            paciente_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

