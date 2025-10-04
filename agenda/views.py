from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from agenda.models import Evento
from agenda.forms import EventoForm


class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "agenda/create_form.html"
    success_url = reverse_lazy("pagina_inicio")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields.pop("estado", None)
        return form
    
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


#====================================================================================

class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = "agenda/update_form.html"
    success_url = reverse_lazy("evento_list")

    def get_queryset(self):
        return Evento.objects.filter(usuario=self.request.user)
  
   

#====================================================================================

class EventoDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = "agenda/detail_form.html"
    context_object_name = "evento"

    def get_queryset(self):
        return Evento.objects.filter(usuario=self.request.user)




#====================================================================================
class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = "agenda/delete_form.html"
    success_url = reverse_lazy("evento_list")

    def get_queryset(self):
        return Evento.objects.filter(usuario=self.request.user)



#====================================================================================
class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "agenda/lista_eventos.html"
    context_object_name = "lista_eventos"

    def get_queryset(self):
        queryset = Evento.objects.filter(usuario=self.request.user).order_by('date_evento')

        estado = self.request.GET.get("estado")
        tipo = self.request.GET.get("tipo")
        fecha_desde = self.request.GET.get("desde")
        fecha_hasta = self.request.GET.get("hasta")

        if estado:
            queryset = queryset.filter(estado=estado)
        if tipo:
            queryset = queryset.filter(tipo_evento=tipo)
        if fecha_desde:
            queryset = queryset.filter(date_evento__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(date_evento__lte=fecha_hasta)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Eventos"
        context['titulo_tabla'] = "Listado de eventos"
        return context
