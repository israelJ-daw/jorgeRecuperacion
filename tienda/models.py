from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):  
    CLIENTE = 1
    ADMIN = 2
    ROLES = (
        (CLIENTE, 'Cliente'),
        (ADMIN, 'Administrador'),
    )
    rol = models.PositiveSmallIntegerField(choices=ROLES, default=CLIENTE)

class Cliente(models.Model):
    usuario = models.CharField(max_length=50) 
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)

class Administrador(models.Model):
    usuario = models.CharField(max_length=50) 
    area_responsabilidad = models.CharField(max_length=100)
