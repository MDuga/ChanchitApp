from django.urls import path
from core import views

urlpatterns = [
    path('registro/', views.crear_usuario, name='crear_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('inicio/', views.pagina_inicio, name='pagina_inicio'),
]
