from django.shortcuts import render

from .models import *
# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def lista_clientes(request):
    clientes = cliente.objects.all()
    
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})