from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', views.index, name='index'),
    path('clientes/', views.lista_clientes,name= 'lista_clientes'),
    path('vendedores/', views.lista_vendedores,name= 'lista_vendedores'),
    path('registro/', views.registrar_usuario, name='registro'), 
    #inicio sesion prederteminado 
    path('login/', auth_views.LoginView.as_view(template_name='registro/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]