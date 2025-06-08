from django.urls import path

from .api_views import *

urlpatterns = [
    path('coches', coche_list),
]
