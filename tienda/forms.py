from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 


class RegistroForm(UserCreationForm):  
    ROLES = (
        (Usuario.CLIENTE, 'cliente'),
        (Usuario.VENDEDOR, 'vendedor'),

    )
    
    rol = forms.ChoiceField(choices=ROLES)

    class Meta:
        model = Usuario  
        fields = ('username', 'email', 'password1', 'password2', 'rol')  
        
    
class cocheModelForms(ModelForm):
    class Meta:
        model = Coche
        fields = ['nombre', 'anyo', 'precio']
        labels = {'nombre' : ("Marca"), 'anyo' : "Año"}
        help_texts = {
            'nombre': ("100 caracteres Maximos"),
            'precio' : ("Escriba un precio realista"), 
        }
        widgets = {'anyo' : forms.DateInput(format="Y-%m-%d", attrs={"type": "date"})}
        
    def clean(self):
        super().clean()
        
        #obetener el campo()
        nombre = self.cleaned_data.get('nombre')
        
        #validaciones
        if len(nombre) < 10:
            self.add_error('nombre', "Mas de 10 caracteres")
             
        return self.cleaned_data     