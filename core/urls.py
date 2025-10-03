from django.urls import path
from core import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),    
    path('inicio/', views.pagina_inicio, name='pagina_inicio'),
    path('ingresos/', views.ingreso_monto, name='ingreso_monto'),
    path('egresos/', views.egreso_monto, name='egreso_monto'),
    path('query/', views.query, name='query'),
    path('update_ingreso/<uuid:uuid>/', views.IngresoUpdateView.as_view(), name="update_ingreso"),
    path('delete_ingreso/<uuid:uuid>/', views.IngresoDeleteView.as_view(), name="delete_ingreso"),
    path('update_egreso/<uuid:uuid>/', views.EgresoUpdateView.as_view(), name="update_egreso"),
    path('delete_egreso/<uuid:uuid>/', views.EgresoDeleteView.as_view(), name="delete_egreso"),

]
