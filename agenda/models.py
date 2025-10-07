from django.db import models
from usuarios.models import Usuario


class Evento(models.Model):

    estados = [
        ("pendiente", "Pendiente"),
        ("cerrado", "Cerrado"),
        ("cancelado", "Cancelado"),
    ]

    tipos_evento = [
        ("cumpleanos", "Cumpleaños"),
        ("entretenimiento", "Hobbies / Entretenimiento"),
        ("viaje", "Viaje"),
        ("regalo", "Regalo"),
        ("otro", "Otro"),
    ]


    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    date_evento = models.DateField()
    tipo_evento = models.CharField(max_length=20, choices=tipos_evento, default="otro")
    monto = models.IntegerField()
    moneda = models.CharField(max_length=3, default='UYU')
    estado = models.CharField(max_length=20, choices=estados, default="pendiente")
    date_creacion = models.DateTimeField(auto_now_add=True)
    date_cierre = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.titulo} ({self.get_estado_display()}) - {self.date_evento}"
