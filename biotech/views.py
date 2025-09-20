from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def telainicial(request):
    return render(request, "telainicial.html")
