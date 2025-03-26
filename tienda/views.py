from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *



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
            # Obtención de los datos del formulario
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))

            # Crear usuario y asignar rol
            if rol == Usuario.CLIENTE:
                cliente = Cliente.objects.create(usuario=user.username)
                cliente.save()
            elif rol == Usuario.ADMIN:
                admin = Administrador.objects.create(usuario=user)
                admin.save()

            # Iniciar sesión del usuario
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()

    return render(request, 'registro/signup.html', {'formulario': formulario})