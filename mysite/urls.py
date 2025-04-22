
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',include('tienda.urls')),
]

from django.conf.urls import handler404, handler500
handler404 = "tienda.views.mi_error_404"
handler500 = "tienda.views.mi_error_500"