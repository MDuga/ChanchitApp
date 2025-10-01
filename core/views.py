from django.shortcuts import render, redirect
from core.models import Ingresos, Egresos
from core.forms import IngresosForm, EgresosForm, QueryMes_Form, QueryFechas_Form
from usuarios.utils import obtener_usuario
from django.contrib import messages
from datetime import date
from calendar import monthrange


def pagina_inicio(request):
    
    usuario = obtener_usuario(request)       
    saldo_actual = 0
    date_actual = date.today()
   
    # movimientos a la fecha
        
    tipo_movimientos = [
    (Ingresos, 'date_ingreso'),
    (Egresos, 'date_egreso')
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
        {"img": "Consultas.png", "alt": "Consultas", "title": "Consultas", "text": "Realiza consulta de movimientos", "url": "query_mes"},
    ]

    contexto = {
        "usuario": usuario,                
        "saldo_actual": saldo_actual,
        "cards": cards
    }
   
    return render(request, 'core/panel/inicio.html', contexto)

#====================================================================

def ingreso_monto(request):
    
    usuario = obtener_usuario(request)

    if request.method == "POST":
        formulario = IngresosForm(request.POST)
        if formulario.is_valid():                     
            ingreso = formulario.save(commit=False)
            ingreso.usuario = usuario
            ingreso.save()
            messages.success(request, "ingreso realizado con éxito.")
            return redirect('pagina_inicio')
    else:
        formulario = IngresosForm()
    
    return render(request, "core/movimientos/ingresos_form.html", {"form": formulario, "usuario": usuario})

#====================================================================

def egreso_monto(request):

    usuario = obtener_usuario(request)

    if request.method == "POST":
        formulario = EgresosForm(request.POST)
        if formulario.is_valid():                     
            egreso = formulario.save(commit=False)
            egreso.usuario = usuario
            egreso.monto = -egreso.monto
            egreso.save()
            messages.success(request, "ingreso realizado con éxito.")
            return redirect('pagina_inicio')
    else:
        formulario = EgresosForm()
    
    return render(request, "core/movimientos/egresos_form.html", {"form": formulario, "usuario": usuario})

#====================================================================
#Auxiliar para query_mes
def fecha_mes(request):
    
    month_year = QueryMes_Form(request.GET or None)
    
    if request.method == "GET" and month_year.is_valid(): 
    # if request.GET and month_year.is_valid(): 
        month = month_year.cleaned_data["month"]
        year = month_year.cleaned_data["year"]        
        date_inicio_mes = date(year, month, 1)
        ultimo_dia = monthrange(year, month)[1]
        date_fin_mes = date(year, month, ultimo_dia)  
    
        return date_inicio_mes, date_fin_mes, month_year
    
    return date(1, 1, 1), date(1, 1, 1), month_year    # se pone como fecha 01/01/01 porque con None da error

#=================================================
#Auxiliar para query_mes
def saldo_inicial_query(request, usuario, date_inicio_mes):    
        
    saldo_inicial = 0

    tipo_movimientos = [
    (Ingresos, 'date_ingreso'),
    (Egresos, 'date_egreso')
    ]

    if request.method == "GET":
         for modelo, campo_fecha in tipo_movimientos:
            filtros = {
            'usuario': usuario,
            f"{campo_fecha}__lt": date_inicio_mes
            }
            modelos_filtrados_list = modelo.objects.filter(**filtros)
                            
            for i in modelos_filtrados_list:                
                saldo_inicial += i.monto       
                

    return saldo_inicial

#=================================================
def query_mes(request):    
    
    usuario = obtener_usuario(request)
    date_inicio_mes, date_fin_mes, month_year = fecha_mes(request)
    
    if not date_inicio_mes:
    
        return render(request, "core/movimientos/query_mes.html", {
            "form": month_year,
            "usuario": usuario,
            "saldo_inicial": 0,
            "movimientos": [],
            "saldo_final": 0
        })
           
    
    saldo_inicial = saldo_inicial_query(request, usuario, date_inicio_mes)      
    saldo_final = 0
    movimientos = []
    movimientos_mes_monto= 0


    tipo_movimientos = [
    (Ingresos, 'date_ingreso', 'Ingresos'),
    (Egresos, 'date_egreso', 'Egresos')
    ]

    if request.method == "GET":
         for modelo, campo_fecha, tipo in tipo_movimientos:
            filtros = {
            'usuario': usuario,
            f"{campo_fecha}__gte": date_inicio_mes,
            f"{campo_fecha}__lte": date_fin_mes
            }
           
            modelos_filtrados_list = modelo.objects.filter(**filtros)
               
            for i in modelos_filtrados_list:                
                movimientos_mes_monto += i.monto
                movimientos.append({
                "tipo": tipo,
                "monto": i.monto,
                "descripcion": i.descripcion,
                "fecha": getattr(i,campo_fecha)
                })
            
    
            saldo_final = saldo_inicial + movimientos_mes_monto
            movimientos.sort(key=lambda x: x["fecha"])

    else:
        messages.error(request, "No hay movimientos para el período seleccionado")

    contexto = {
        "usuario": usuario,        
        "form": month_year,
        "saldo_inicial": saldo_inicial,
        "movimientos": movimientos,
        "saldo_final": saldo_final
    }
    return render(request, "core/movimientos/query_mes.html", contexto)

#====================================================================================
def pagina_principal(request):

    return render(request, 'core/panel/principal.html')

#====================================================================================

            