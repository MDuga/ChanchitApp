from django.urls import path
from core import views

urlpatterns = [
    path('registro/', views.crear_usuario, name='crear_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('inicio/', views.pagina_inicio, name='pagina_inicio'),
    path('ingresos/', views.ingreso_monto, name='ingreso_monto'),
    path('egresos/', views.egreso_monto, name='egreso_monto'),
    path('query_mes/', views.query_mes, name='query_mes'),
]
