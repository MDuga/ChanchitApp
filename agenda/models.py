from django.db import models
from usuarios.models import Usuario
from django.utils import timezone

class Evento(models.Model):

    estados = [
        ("pendiente", "Pendiente"),
        ("cerrado", "Cerrado"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    date_evento = models.DateField()
    monto = models.IntegerField()
    moneda = models.CharField(max_length=3, default='UYU')
    estado = models.CharField(max_length=20, choices=estados, default="pendiente")
    date_creacion = models.DateTimeField(auto_now_add=True)
    date_cierre = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.descripcion} ({self.get_estado_display()}) - {self.date_evento}"
