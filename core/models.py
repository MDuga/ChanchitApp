from django.db import models

class Usuario(models.Model):
    username = models.CharField(max_length=100, unique = True)
    email = models.EmailField(max_length=100, unique = True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} con la dirección de correo electrónico: {self.email} se unió a la app el día: {self.date_joined}"