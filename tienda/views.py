from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.models import Group



from .models import *
# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def lista_clientes(request):
    clientes = Cliente.objects.all()
    
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})


def registrar_usuario(request):

    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if (rol == Usuario.CLIENTE):
                grupo = Group.objects.get(name='clientes')
                grupo.user_set.add(user)
                cliente = Cliente.objects.create(Usuario=user)
                cliente.save()
            elif (rol == Usuario.VENDEDOR):
                grupo=Group.objects.get(name='vendedores')
                grupo.user_set.add(user)
                vendedor= Vendedor.objects.create(Usuario=user)
                vendedor.save()
                
            login(request,user)    
            return redirect('index')
        
    else:
        formulario = RegistroForm()   
    return render(request, 'registro/signup.html', {'formulario': formulario})


def lista_vendedores(request):
    vendedores = Vendedor.objects.all()

    return render (request, 'vendedores/lista_vendedores.html', {'vendedores': vendedores})