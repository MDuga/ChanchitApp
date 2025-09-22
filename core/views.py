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
    return render(request, 'core/panel/inicio.html', {"usuario": usuario})

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

def query_mes(request):    
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.get(id=usuario_id)
    
    saldo_inicial = 0
    saldo_final = 0
    movimientos = []
    
    if request.method == "GET":
        query_mes = QueryMes_Form(request.GET)
        if query_mes.is_valid():  
            month = query_mes.cleaned_data["month"]
            year = query_mes.cleaned_data["year"]
            date_inicio_mes = date(year, month, 1) 

    # saldo inicial
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

        # movimientos del mes 
            
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
        "form": query_mes,
        "saldo_inicial": saldo_inicial,
        "movimientos": movimientos,
        "saldo_final": saldo_final
    }
    return render(request, "core/movimientos/query_mes.html", contexto)
            
            
            