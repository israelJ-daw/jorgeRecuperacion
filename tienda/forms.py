from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):  
    ROLES = (
        (Usuario.CLIENTE, 'Cliente'),
        (Usuario.ADMIN, 'Administrador'),
    )
    
    rol = forms.ChoiceField(choices=ROLES)

    class Meta:
        model = Usuario  
        fields = ('username', 'email', 'password1', 'password2', 'rol')  