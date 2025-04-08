from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', views.index, name='index'),
    path('clientes/', views.lista_clientes,name= 'lista_clientes'),
    path('vendedores/', views.lista_vendedores,name= 'lista_vendedores'),
    path('registro/', views.registrar_usuario, name='registro'), 
    path('coches/', views.lista_coches, name='lista_coche'), 
    path('crear/coches/', views.crear_coche, name='crear_coche'), 
    path('crear/tienda/', views.crear_tienda, name='crear_tienda'), 
    path('tiendas/', views.lista_tienda,name= 'lista_tienda'),
    path('coche/<int:id_coche>', views.coche_detalle, name='coche_detalle'),
    path('coche/<int:id_coche>/editar', views.coche_editar, name='coche_editar'),
] 
