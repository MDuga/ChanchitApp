from django.contrib import admin
from .models import Usuario, Ingresos, Egresos

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Ingresos)
admin.site.register(Egresos)
