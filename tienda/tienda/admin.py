from django.contrib import admin
from .models import Usuario, Cliente, Empleado, Direccion

# Registramos los modelos para que aparezcan en el panel /admin
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Direccion)