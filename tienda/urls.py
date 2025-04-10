from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', views.index, name='index'),
    path('clientes/', views.lista_clientes,name= 'lista_clientes'),
    path('vendedores/', views.lista_vendedores,name= 'lista_vendedores'),
    path('registro/', views.registrar_usuario, name='registro'), 
    #coches
    path('coches/', views.lista_coches, name='lista_coche'), 
    path('crear/coches/', views.crear_coche, name='crear_coche'), 
    path('coche/<int:id_coche>', views.coche_detalle, name='coche_detalle'),
    path('coche/<int:id_coche>/editar', views.coche_editar, name='coche_editar'),
    path('coche/eliminar/<int:id_coche>', views.coche_eliminar, name= 'coche_eliminar'),
    #tiendas
    path('crear/tienda/', views.crear_tienda, name='crear_tienda'), 
    path('tiendas/', views.lista_tienda,name= 'lista_tienda'),
    path('tienda/<int:id_tienda>', views.tienda_detalle, name='tienda_detalle'),
    path('tienda/<int:id_tienda>/editar', views.tienda_editar, name='tienda_editar'),
    #Cliente
    path('detalle/cliente/<int:id_cliente>', views.detalle_cliente,name= 'detalle_cliente'),
    #cuenta
    path ('ver/cuenta/<int:id_cliente>', views.ver_cuenta, name = 'ver_cuenta'),
    path('crear/cuenta/', views.crear_cuenta, name='crear_cuenta'), 

] 
