from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from agenda.models import Evento
from agenda.forms import EventoForm
from core.utils import *
from datetime import date
import calendar
from calendar import monthrange


MESES = [
        "",
        "Enero", 
        "Febrero", 
        "Marzo", 
        "Abril", 
        "Mayo", 
        "Junio", 
        "Julio", 
        "Agosto", 
        "Setiembre", 
        "Octubre", 
        "Noviembre", 
        "Diciembre"
        ]

#====================================================================================
class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "agenda/create_form.html"
    success_url = reverse_lazy("evento_list")

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
def datos_calendario_actual(request):
    
    date_actual = date.today()
    cal = calendar.Calendar(firstweekday=0)
        
    month_actual = date_actual.month
    year_actual = date_actual.year
    last_day_actual = monthrange(year_actual, month_actual)[1]
    last_date_actual = date(year_actual, month_actual, last_day_actual)  

    name_month_actual = MESES[month_actual]
    weeks_actual = cal.monthdayscalendar(year_actual, month_actual)


    return (date_actual, month_actual, year_actual, last_date_actual, name_month_actual, weeks_actual)

#====================================================================================

def datos_calendario_next(request, month_actual, year_actual):
    
    date_actual = date.today()
    cal = calendar.Calendar(firstweekday=0)

    if month_actual=="12":
        month_next = "1"
        year_next = year_actual + 1
            
    month_next = month_actual + 1
    year_next = year_actual

    last_day_next = monthrange(year_next, month_next)[1]
    last_date_next = date(year_next, month_next, last_day_next)  

    name_month_next = MESES[month_next]
        
    weeks_next = cal.monthdayscalendar(year_next, month_next)

    return (month_next, year_next, last_date_next, name_month_next, weeks_next)


#====================================================================================
def resumen_mensual(request):
    
    #Variables
    usuario = request.user
    date_actual, month_actual, year_actual, last_date_actual, name_month_actual, weeks_actual = datos_calendario_actual(request)
    month_next, year_next, last_date_next, name_month_next, weeks_next = datos_calendario_next(request, month_actual, year_actual)
    saldo = saldo_actual(usuario).get("saldo_actual", 0)


    evento_monto_actual = 0
    evento_monto_next = 0
    eventos_actual = []
    eventos_next = []
    eventos_actual_day = []
    eventos_next_day = []
    contexto_actual = {}
    contexto_next = {}

   
    if request.method == "GET":
        filtro_actual = {
            'usuario': usuario,
            'date_evento__gte': date_actual,
            'date_evento__lte': last_date_actual
        }
        eventos_actual_list = Evento.objects.filter(**filtro_actual).exclude(estado="cancelado")
                           
        for i in eventos_actual_list:                            
            eventos_actual.append(i)
            eventos_actual_day.append(i.date_evento.day)
            if i.estado == "pendiente":
                evento_monto_actual += i.monto
        
        faltante_actual = evento_monto_actual - saldo
        eventos_actual.sort(key=lambda x: x.date_evento)
        
        if faltante_actual > 0:
            mensaje = f"¡Ánimo! Te faltan {faltante_actual} UYU para llegar a tu meta."
        else:
            mensaje = "¡Buen trabajo! Alcanzaste tu meta para este mes."

    
        contexto_actual = {                             
            "eventos_actual": eventos_actual,
            "evento_monto_actual": evento_monto_actual,
            "eventos_actual_day": eventos_actual_day,
            "faltante_actual": faltante_actual,
            "mensaje": mensaje,
            "name_month_actual": name_month_actual,
            "year_actual": year_actual,
            "weeks_actual": weeks_actual,
            "saldo_actual": saldo
        }
    
        filtro_next = {
            'usuario': usuario,
            'date_evento__gt': last_date_actual,
            'date_evento__lte': last_date_next
        }
        eventos_next_list = Evento.objects.filter(**filtro_next).exclude(estado="cancelado")

        
        for i in eventos_next_list:                            
            eventos_next.append(i)
            eventos_next_day.append(i.date_evento.day)
            if i.estado == "pendiente":
                evento_monto_next += i.monto
        
        eventos_next.sort(key=lambda x: x.date_evento)
    
        contexto_next = {                
            "eventos_next": eventos_next,
            "eventos_next_day": eventos_next_day,
            "evento_monto_next": evento_monto_next,
            "name_month_next": name_month_next,
            "year_next": year_next,
            "weeks_next": weeks_next
            }
         
    contexto = contexto_actual|contexto_next

    return contexto

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
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = "Eventos"
        contexto['titulo_tabla'] = "Listado de eventos"

        resumen = resumen_mensual(self.request)
        contexto.update(resumen)
        return contexto