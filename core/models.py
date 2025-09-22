from django.db import models

class Usuario(models.Model):
    usuario = models.CharField(max_length=100, unique = True)
    email = models.EmailField(max_length=100, unique = True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} con la dirección de correo electrónico: {self.email} se unió a la app el día: {self.date_joined}"
    
#========================================================================================
class Ingresos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.IntegerField()
    moneda = models.CharField(max_length=3, default='UYU')
    descripcion = models.CharField(max_length=100)
    date_ingreso = models.DateField()
    date_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} realizó el siguiente ingreso: {self.moneda} {self.monto} con fecha: {self.date_ingreso}"
    
#========================================================================================
class Egresos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.IntegerField()
    moneda = models.CharField(max_length=3, default='UYU')
    descripcion = models.CharField(max_length=100)
    date_egreso = models.DateField()
    date_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} realizó el siguiente consumo: {self.moneda} {self.monto} con fecha: {self.date_egreso}"