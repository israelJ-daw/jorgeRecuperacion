from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from datetime import datetime



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
        widgets = {'anyo' : forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})}
        
    def clean(self):
        super().clean()
        
        #obetener el campo()
        nombre = self.cleaned_data.get('nombre')
        anyo = self.cleaned_data.get('anyo')
        anyo_actual =  datetime.now().year
        precio= self.cleaned_data.get('precio')
        
        #validaciones
        if len(nombre) < 10:
            self.add_error('nombre', "Mas de 10 caracteres")

        if precio < 0:
            self.add_error('precio' , 'El precio tiene que ser mayor de 0!')

        if anyo.year < 1886 or anyo.year > anyo_actual:
            self.add_error('anyo', 'El año debe estar entre 1886 y ' + str(anyo_actual))


        return self.cleaned_data  


class TiendaModelForms(ModelForm):
    class Meta:
        model = Tienda
        fields = ['nombre' , 'direccion' , 'telefono']
        help_texts = {
            'nombre' : ("Nombre de la tienda"),
            'direccion': ("Direccion de la tienda")
        }

    def clean(self):
        super().clean()

        nombre = self.cleaned_data.get('nombre')
        direccion = self.cleaned_data.get('direccion')
        telefono= self.cleaned_data.get('telefono')

        if len(nombre) < 10:
            self.add_error('nombre', "Mas de 10 caracteres")

        if len(direccion) < 10:
            self.add_error('direccion', "Especifica donde se encuentra la tienda")

        if len(telefono) < 5:
            self.add_error('telefono', "Escriba un telefono Real!!")
            
class CuentaModelForms(ModelForm):
    class Meta:
        model = CuentaBancaria 
        fields = ['iban', 'banco', 'tipo']  
        help_texts = {
            'iban' : ("IBAN de la cuenta "),
            'banco': ("Escriba su Banco favorito")
        }        

class DatosModelForms(ModelForm):
    class Meta:
        model = DatosVendedor 
        fields = ['direccion', 'facturacion']  
        help_texts = {
            'direccion' : ("Direccion del vendedor"),
            'facturacion': ("Escriba su Facturacion")
        }        
        
        
        
        
class CrearInventarioForms(ModelForm):
    class Meta:
        model = Inventario
        fields = ['tienda' , 'coches', 'cantidad' , 'precio']
        help_texts = {
            'tienda' : ("indica la tienda que es"),
            'cantidad' : ("Cantidad de coches")
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CrearInventarioForms, self).__init__ (*args, **kwargs)
        tiendasDisponibles = Tienda.objects.filter(vendedor = self.request.user.vendedor).all()
        self.fields["tienda"] = forms.ModelChoiceField(
            queryset=tiendasDisponibles,
            widget=forms.Select,
            required=True,
            empty_label="Ninguna"
        )


class BusquedaInventario(forms.Form):
    nombre = forms.CharField(required=False)

class CrearPedidoForms(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['coche', 'cantidad', 'direccion']
        help_texts = {
            'coche': "Elija el Coche que desea",
        }
        widgets = {
            'fecha_pedido': forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
        }


class cantidadComprar(forms.Form):
    cantidad = forms.IntegerField (required=True)
    direccion = forms.CharField(max_length = 100)