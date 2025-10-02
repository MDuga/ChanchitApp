from django.shortcuts import render, redirect
from usuarios.models import Usuario
from usuarios.forms import RegistroForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login


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

    return render(request, "usuarios/usuario_form.html", {"form": formulario})

#=========================================================================

# def login_usuario(request):
#     if request.method == "POST":
#         formulario = LoginForm(request.POST)
#         if formulario.is_valid(): 
#             email = formulario.cleaned_data["email"] 
#             usuario = Usuario.objects.get(email=email) 
#             request.session["usuario_id"] = usuario.id           
#             messages.success(request, "Login realizado con éxito.")
#             return redirect('pagina_inicio')
#     else:
#         formulario = LoginForm()
    
#     return render(request, "usuarios/login_form.html", {"form": formulario})


def login_usuario(request):
    if request.method == "POST":
        formulario = LoginForm(request.POST)
        if formulario.is_valid(): 
            usuario = formulario.user
            login (request, usuario)
            return redirect('pagina_inicio')
          
    else:
        formulario = LoginForm()
    
    return render(request, "usuarios/login_form.html", {"form": formulario})