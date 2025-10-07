from django.urls import path
from agenda import views


urlpatterns = [
path('evento/list/', views.EventoListView.as_view(), name="evento_list"),
path('evento/create/', views.EventoCreateView.as_view(), name="evento_create"),
path('evento/<int:pk>/update/', views.EventoUpdateView.as_view(), name="evento_update"),
path('evento/<int:pk>/delete/', views.EventoDeleteView.as_view(), name="evento_delete"),
path('evento/<int:pk>/detail/', views.EventoDetailView.as_view(), name="evento_detail"),
]