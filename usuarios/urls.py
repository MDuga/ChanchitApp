from django.urls import path
from usuarios import views

urlpatterns = [           
    path('registro/', views.crear_usuario, name='crear_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('perfil/', views.vista_perfil, name='vista_perfil'),
    path('logout/', views.cerrar_sesion, name='logout')    
]




