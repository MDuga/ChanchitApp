from django.shortcuts import render, redirect
from core.models import Usuario, Ingresos, Egresos
from core.forms import RegistroForm, LoginForm, IngresosForm, EgresosForm, QueryMes_Form, QueryFechas_Form
from django.contrib import messages
from datetime import date

#from django.contrib.auth import authenticate, login

# Create your views here.

def crear_usuario(request):
    if request.method == "POST":
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            email = formulario.cleaned_data["email"] 
            usuario = Usuario.objects.get(email=email) 
            request.session["usuario_id"] = usuario.id
            messages.success(request, "Usuario registrado con éxito.")
            return redirect('pagina_inicio')
    else: 
        formulario = RegistroForm()

    return render(request, "core/usuarios/usuario_form.html", {"form": formulario})

#=========================================================================

def login_usuario(request):
    if request.method == "POST":
        formulario = LoginForm(request.POST)
        if formulario.is_valid(): 
            email = formulario.cleaned_data["email"] 
            usuario = Usuario.objects.get(email=email) 
            request.session["usuario_id"] = usuario.id           
            messages.success(request, "Login realizado con éxito.")
            return redirect('pagina_inicio')
    else:
        formulario = LoginForm()
    
    return render(request, "core/usuarios/login_form.html", {"form": formulario})
#====================================================================
def pagina_inicio(request):
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.get(id=usuario_id)
        
    saldo_actual = 0
    date_actual = date.today()
   
    # movimientos a la fecha
        
    ingresos_actual_list = Ingresos.objects.filter(
        usuario = usuario, 
        date_ingreso__lte = date_actual    
        )
    
    ingresos_actual = 0
    for i in ingresos_actual_list:                
        ingresos_actual += i.monto


    egresos_actual_list = Egresos.objects.filter(
        usuario = usuario, 
        date_egreso__lte = date_actual
        )  
    
    egresos_actual = 0
    for e in egresos_actual_list:                
        egresos_actual += e.monto   
       
    saldo_actual = ingresos_actual + egresos_actual
    
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
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.get(id=usuario_id)
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
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.get(id=usuario_id)
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
#Auxiliar para query_mes - Nº1
def obtener_usuario(request):
    usuario_id = request.session.get("usuario_id")
    return Usuario.objects.get(id=usuario_id)
    
#=================================================
#Auxiliar para query_mes - Nº2
def fecha_inicio_mes(request):
    month_year = QueryMes_Form(request.GET or None)
    if request.method == "GET" and month_year.is_valid(): 
    # if request.GET and month_year.is_valid(): 
        month = month_year.cleaned_data["month"]
        year = month_year.cleaned_data["year"]  
        date_inicio_mes = date(year, month, 1)
    
        return date_inicio_mes, year, month, month_year
    
    return date(1, 1, 1), 1, 1, month_year    # se pone como fecha 01/01/01 porque con None da error

#=================================================
#Auxiliar para query_mes - Nº3
def saldo_inicial_query(request, usuario, date_inicio_mes):    
    
    saldo_inicial = 0
    if request.method == "GET":
        ingresos_saldo_inicio = Ingresos.objects.filter(
            usuario = usuario, 
            date_ingreso__lt = date_inicio_mes    
            )

        egresos_saldo_inicio = Egresos.objects.filter(
            usuario = usuario, 
            date_egreso__lt = date_inicio_mes          
            )

        ingresos_saldo_monto= 0
        for i in ingresos_saldo_inicio:                
            ingresos_saldo_monto += i.monto

        egresos_saldo_monto = 0
        for e in egresos_saldo_inicio:                
            egresos_saldo_monto += e.monto

    saldo_inicial = ingresos_saldo_monto + egresos_saldo_monto
    return saldo_inicial

#=================================================
def query_mes(request):    
    
    usuario = obtener_usuario(request)
    date_inicio_mes, year, month, month_year = fecha_inicio_mes(request)
    
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
    
    if request.method == "GET":            
        ingresos_list = Ingresos.objects.filter(
            usuario = usuario, 
            date_ingreso__month = month, 
            date_ingreso__year = year
            )
        
        egresos_list = Egresos.objects.filter(
            usuario = usuario, 
            date_egreso__month = month, 
            date_egreso__year = year
            )                   

        ingresos_mes_monto= 0
        for i in ingresos_list:                
            ingresos_mes_monto += i.monto
            movimientos.append({
            "tipo": "Ingreso",
            "monto": i.monto,
            "descripcion": i.descripcion,
            "fecha": i.date_ingreso
            })
        
        egresos_mes_monto = 0
        for e in egresos_list:                
            egresos_mes_monto += e.monto
            movimientos.append({
            "tipo": "Egreso",
            "monto": e.monto,
            "descripcion": e.descripcion,
            "fecha": e.date_egreso
            })
        
        saldo_final = ingresos_mes_monto + egresos_mes_monto + saldo_inicial
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

            