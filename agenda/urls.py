from django.urls import path
from agenda.views import *


urlpatterns = [
path('evento/list/', EventoListView.as_view(), name="evento_list"),
path('evento/create/', EventoCreateView.as_view(), name="evento_create"),
path('evento/<int:pk>/update/', EventoUpdateView.as_view(), name="evento_update"),
path('evento/<int:pk>/delete/', EventoDeleteView.as_view(), name="evento_delete"),
path('evento/<int:pk>/detail/', EventoDetailView.as_view(), name="evento_detail"),
]