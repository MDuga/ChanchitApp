from django.contrib import admin
from usuarios.models import Usuario
from core.models import Ingresos, Egresos

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Ingresos)
admin.site.register(Egresos)
