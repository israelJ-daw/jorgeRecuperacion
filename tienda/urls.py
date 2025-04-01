from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', views.index, name='index'),
    path('clientes/', views.lista_clientes,name= 'lista_clientes'),
    path('vendedores/', views.lista_vendedores,name= 'lista_vendedores'),
    path('registro/', views.registrar_usuario, name='registro'), 
] 
