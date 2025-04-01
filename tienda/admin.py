from django.contrib import admin

from .models import *

#añadir 1 a 1 cada modelo que queremos administrar en admin

admin.site.register(Cliente)
admin.site.register(Usuario)
admin.site.register(Vendedor)
admin.site.register(Coche)




