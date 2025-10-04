from django.urls import path
from usuarios import views

urlpatterns = [           
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('perfil/', views.vista_perfil, name='vista_perfil'),
    path('logout/', views.cerrar_sesion, name='logout')    
]




