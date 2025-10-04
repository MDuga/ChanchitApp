from django.db import models
from usuarios.models import Usuario
import uuid

class Ingresos(models.Model):
    
    categorias_ingresos = [
        ("sueldo", "Sueldo / mesada"),
        ("regalo", "Regalos"),
        ("otro", "Otros ingresos"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.IntegerField()
    moneda = models.CharField(max_length=3, default='UYU')
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=categorias_ingresos)
    date_movimiento = models.DateField()
    date_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} realizó el siguiente ingreso: {self.moneda} {self.monto} con fecha: {self.date_movimiento}"
    
#========================================================================================
class Egresos(models.Model):

    categorias_egresos = [
        ("hobbies", "Hobbies"),
        ("entretenimiento", "Entretenimiento"),
        ("ropa", "Ropa"),
        ("regalos", "Regalos"),
        ("estudio", "Estudio"),
        ("transporte", "Transporte"),        
        ("otros", "Otros gastos"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.IntegerField()
    moneda = models.CharField(max_length=3, default='UYU')
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=categorias_egresos)
    date_movimiento = models.DateField()
    date_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} realizó el siguiente consumo: {self.moneda} {self.monto} con fecha: {self.date_movimiento}"