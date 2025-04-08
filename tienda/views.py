from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

from .models import *
# Create your views here.

def index(request):
    return render(request, 'index.html', {})

@permission_required('tienda.view_cliente')
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
    return render(request, 'registration/signup.html', {'formulario': formulario})


def lista_vendedores(request):
    vendedores = Vendedor.objects.all()

    return render (request, 'vendedores/lista_vendedores.html', {'vendedores': vendedores})


def lista_coches(request):
    coches = Coche.objects.all()

    return render (request, 'coches/lista_coche.html', {'coches': coches})

permission_required('tienda.add_coche')
def crear_coche(request):
    if request.method == 'POST':
        formulario = cocheModelForms(request.POST)
        if formulario.is_valid():
            print ("Es validoo!")
            formulario.save()
            messages.success(request, 'Se ha creado perfectamente')
            return redirect ("lista_coche")
    else:
        formulario = cocheModelForms()
    return render (request, 'coches/crear_coche.html', {'formulario': formulario})


def crear_tienda(request):
    if request.method == 'POST':
        formulario = TiendaModelForms(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect ("lista_tienda")
    else:
        formulario = TiendaModelForms()

    return render (request, 'tienda/crear_tienda.html', {'formulario': formulario})
    

def lista_tienda(request):
    tiendas = Tienda.objects.all() 
    return render(request, 'tienda/lista_tienda.html', {'tiendas': tiendas})


def coche_detalle(request, id_coche):
    coche = Coche.objects.get(id=id_coche)
    return render (request, 'coches/coche_detalle.html',{'coche' : coche}) 

def coche_editar(request, id_coche):
    coche = Coche.objects.get(id = id_coche)
    
    if request.method == "POST": 
        formulario = cocheModelForms(request.POST, instance=coche)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, 'Se ha modificado perfectamente')            
            return redirect ('coche_detalle', id_coche=id_coche) 
    else:
        formulario = cocheModelForms(instance=coche)     
        
    return render (request, 'coches/coche_editar.html', {'formulario' : formulario, 'lola' : coche })   