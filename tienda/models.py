from django.db import models

# Create your models here.


class cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50)
    
    
    