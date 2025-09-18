from django.urls import path
from core import views

urlpatterns = [
    path('', views.crear_usuario, name='crear_usuario'),
]
