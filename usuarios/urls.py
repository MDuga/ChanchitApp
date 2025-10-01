from django.urls import path
from usuarios import views

urlpatterns = [       
    path('registro/', views.crear_usuario, name='crear_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),    
]




