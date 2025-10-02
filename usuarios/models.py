from django.contrib.auth.models import AbstractUser
from django.db import models
import os
import uuid

def user_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("avatars",str(instance.id), filename)


class Usuario(AbstractUser):     
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        default="avatars/default.png",
        blank=True,
        null=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    
    def __str__(self):
        return f"{self.username} con la dirección de correo electrónico: {self.email} se unió a la app el día: {self.date_joined}"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = "avatars/default.png"
        super().save(*args, **kwargs)


