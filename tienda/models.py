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
  nombre = models.CharField(max_length=50),
  anyo = models.DateField(auto_now=False, auto_now_add=False)
  precio = models.FloatField()