from django.shortcuts import render, redirect
from core.models import Usuario
from core.forms import RegistroForm
from django.contrib import messages
from core.forms import LoginForm
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