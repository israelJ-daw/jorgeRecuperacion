from django.shortcuts import render

from .models import *
# Create your views here.


def lista_clientes(request):
    clientes = cliente.objects.all()
    
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})