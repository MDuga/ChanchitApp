from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from core.models import Ingresos, Egresos
from core.forms import IngresosForm, EgresosForm, QueryMes_Form, QueryFechas_Form
from datetime import date
from calendar import monthrange


#====================================================================================
def pagina_principal(request):

    return render(request, 'core/panel/principal.html')

#====================================================================================

@login_required
def pagina_inicio(request):
    
    usuario = request.user
    saldo_actual = 0
    date_actual = date.today()
   
            
    tipo_movimientos = [
    (Ingresos, 'date_movimiento'),
    (Egresos, 'date_movimiento')
    ]

    for modelo, campo_fecha in tipo_movimientos:
        filtros = {
            'usuario': usuario,
            f"{campo_fecha}__lte": date_actual
        }
        modelos_filtrados_list = modelo.objects.filter(**filtros)
                
        for i in modelos_filtrados_list:                
            saldo_actual += i.monto
        
    
    #CARDS para template

    cards = [
        {"img": "Ingresos.png", "alt": "Ingresos", "title": "Ingresos", "text": "Registra entradas de dinero", "url": "ingreso_monto"},
        {"img": "Egresos.png", "alt": "Egresos", "title": "Egresos", "text": "Registra salidas de dinero", "url": "egreso_monto"},
        {"img": "Consultas.png", "alt": "Consultas", "title": "Consultas", "text": "Realiza consulta de movimientos", "url": "query"},
    ]

    contexto = {
        "usuario": usuario,                
        "saldo_actual": saldo_actual,
        "cards": cards
    }
   
    return render(request, 'core/panel/inicio.html', contexto)

#====================================================================
@login_required
def ingreso_monto(request):
    
    usuario = request.user

    if request.method == "POST":
        formulario = IngresosForm(request.POST)
        if formulario.is_valid():                     
            ingreso = formulario.save(commit=False)
            ingreso.usuario = usuario
            ingreso.save()
            messages.success(request, "Ingreso realizado con éxito.")
            return redirect('pagina_inicio')
    else:
        formulario = IngresosForm()
    
    return render(request, "core/movimientos/ingresos_form.html", {"form": formulario, "usuario": usuario})

#====================================================================
@login_required
def egreso_monto(request):

    usuario = request.user

    if request.method == "POST":
        formulario = EgresosForm(request.POST)
        if formulario.is_valid():                     
            egreso = formulario.save(commit=False)
            egreso.usuario = usuario
            egreso.save()
            messages.success(request, "Egreso realizado con éxito.")
            return redirect('pagina_inicio')
    else:
        formulario = EgresosForm()
    
    return render(request, "core/movimientos/egresos_form.html", {"form": formulario, "usuario": usuario})

#====================================================================
@login_required
def seleccion_query(request):
    month_year = QueryMes_Form(request.GET or None)
    rango_fechas = QueryFechas_Form(request.GET or None)
    
    if month_year.is_valid(): 
        month = month_year.cleaned_data["month"]
        year = month_year.cleaned_data["year"]        
        date_inicio = date(year, month, 1)
        ultimo_dia = monthrange(year, month)[1]
        date_fin = date(year, month, ultimo_dia)  
    
        return date_inicio, date_fin, month_year, rango_fechas
    
    elif rango_fechas.is_valid():
        date_inicio = rango_fechas.cleaned_data["inicio"]
        date_fin = rango_fechas.cleaned_data["fin"]
        
        return date_inicio, date_fin, month_year, rango_fechas        

    
    return date(1, 1, 1), date(1, 1, 1), month_year, rango_fechas    # se pone como fecha 01/01/01 porque con None da error

#=================================================
#Auxiliar para query_mes
@login_required
def saldo_inicial_query(request, usuario, date_inicio):    
        
    saldo_inicial = 0

    tipo_movimientos = [
    (Ingresos, 'date_movimiento'),
    (Egresos, 'date_movimiento')
    ]
    
    for modelo, campo_fecha in tipo_movimientos:
        filtros = {
        'usuario': usuario,
        f"{campo_fecha}__lt": date_inicio
        }
        modelos_filtrados_list = modelo.objects.filter(**filtros)
                        
        for i in modelos_filtrados_list:                
            saldo_inicial += i.monto       
                

    return saldo_inicial


#====================================================================================

@login_required
def query(request):    
    usuario = request.user

    if not request.GET:  
        return render(request, "core/movimientos/query.html", {
            "usuario": usuario,
            "form_mes": QueryMes_Form(),    
            "form_fechas": QueryFechas_Form(),
            "saldo_inicial": None,           
            "movimientos": None,           
            "saldo_final": None
        })

    date_inicio, date_fin, month_year, rango_fechas = seleccion_query(request)
      
    if date_inicio == date(1, 1, 1) and date_fin == date(1, 1, 1):
        return render(request, "core/movimientos/query.html", {
            "usuario": usuario,
            "form_mes": month_year,
            "form_fechas": rango_fechas,            
            "saldo_inicial": 0,
            "movimientos": [],
            "saldo_final": 0
        })
           
    saldo_inicial = saldo_inicial_query(request, usuario, date_inicio)      
    saldo_final = 0
    movimientos = []
    movimientos_monto = 0

    tipo_movimientos = [
        (Ingresos, 'date_movimiento', 'Ingresos'),
        (Egresos, 'date_movimiento', 'Egresos')
    ]

    if request.method == "GET":
        for modelo, campo_fecha, tipo in tipo_movimientos:
            filtros = {
                'usuario': usuario,
                f"{campo_fecha}__gte": date_inicio,
                f"{campo_fecha}__lte": date_fin
            }
            modelos_filtrados_list = modelo.objects.filter(**filtros)
               
            for i in modelos_filtrados_list:                
                i.tipo_modelo = tipo  
                movimientos_monto += i.monto
                movimientos.append(i)
            
        saldo_final = saldo_inicial + movimientos_monto
        movimientos.sort(key=lambda x: x.date_movimiento)
    else:
        messages.error(request, "No hay movimientos para el período seleccionado")

    contexto = {
        "usuario": usuario,              
        "form_mes": month_year,
        "form_fechas": rango_fechas,
        "saldo_inicial": saldo_inicial,
        "movimientos": movimientos,
        "saldo_final": saldo_final
    }
    return render(request, "core/movimientos/query.html", contexto)


#====================================================================================

class IngresoUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingresos
    template_name = "core/movimientos/ingresos_form.html"
    form_class = IngresosForm
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    success_url = reverse_lazy("query")

    def get_queryset(self):
        return Ingresos.objects.filter(usuario=self.request.user)


#====================================================================================
class EgresoUpdateView(LoginRequiredMixin, UpdateView):
    model = Egresos
    template_name = "core/movimientos/egresos_form.html"
    form_class = EgresosForm
    #fields = ["monto", "descripcion", "categoria", "date_movimiento"]
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    success_url = reverse_lazy("query")

    def get_queryset(self):
        return Egresos.objects.filter(usuario=self.request.user)


#====================================================================================
class IngresoDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingresos
    template_name = "core/movimientos/delete_confirmation_form.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    success_url = reverse_lazy("query")

    def get_queryset(self):
        return Ingresos.objects.filter(usuario=self.request.user)


#====================================================================================
class EgresoDeleteView(LoginRequiredMixin, DeleteView):
    model = Egresos
    template_name = "core/movimientos/delete_confirmation_form.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    success_url = reverse_lazy("query")

    def get_queryset(self):
        return Egresos.objects.filter(usuario=self.request.user)