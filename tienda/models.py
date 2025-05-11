from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):  
    ADMINISTRADOR = 1
    CLIENTE = 2
    VENDEDOR = 3
    ROLES = (
        (ADMINISTRADOR, 'administrador'),
        (CLIENTE, 'cliente'),
        (VENDEDOR, 'Vendedor')
    )
    rol = models.PositiveSmallIntegerField(choices=ROLES, default=CLIENTE)





class Cliente(models.Model):
  
  Usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
  
  def __str__(self):
     return self.Usuario.username


class Vendedor(models.Model):
    
  Usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

   
  def __str__(self):
     return self.Usuario.username


class Coche(models.Model):
  nombre = models.CharField(max_length=50)
  anyo = models.DateField(auto_now=False, auto_now_add=False)
  precio = models.FloatField()
    
  def __str__(self):
    return self.nombre

class Tienda(models.Model):
  nombre = models.CharField(max_length=50) 
  direccion = models.CharField(max_length=100) 
  telefono = models.CharField(max_length=30)
  vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, default=None, null=True)  
  
  productos = models.ManyToManyField(Coche, through="Inventario")
  
  def __str__(self):
    return self.nombre
  
  
class CuentaBancaria(models.Model):
  iban = models.CharField(max_length=50)
  banco = models.CharField(max_length=50)
  MONEDA = [
    ("EU" , "Euros"),
    ("Dolar" , "Dolar"),
    ("LIB" , "Libra")
  ]
  tipo = models.CharField(
    max_length=5, choices=MONEDA,default="EU"
  )
  
  cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

class DatosVendedor(models.Model):
  direccion = models.CharField(max_length=50)
  facturacion = models.CharField(max_length=50)

  vendedor = models.OneToOneField(Vendedor, on_delete=models.CASCADE)
  
  
class Inventario(models.Model):
  tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
  coches = models.ForeignKey(Coche, on_delete=models.CASCADE)
  cantidad = models.IntegerField(default=0)


class Pedidos(models.Model):
  cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
  coche = models.ForeignKey(Coche, on_delete=models.CASCADE)

  fecha_pedido = models.DateTimeField(auto_now_add=True)
  cantidad = models.PositiveIntegerField(default=1)
  direccion = models.CharField(max_length=255)
