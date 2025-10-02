from django.shortcuts import render, redirect
from usuarios.forms import RegistroForm, LoginForm, UsuarioEditForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required

User = get_user_model()

def crear_usuario(request):
    if request.method == "POST":
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            messages.success(request, "Usuario registrado con éxito.")
            return redirect('pagina_inicio')
    else: 
        formulario = RegistroForm()

    return render(request, "usuarios/registro_form.html", {"form": formulario})

#=========================================================================
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

#=========================================================================

def cerrar_sesion(request):
    logout(request)
    return redirect('pagina_principal')

#=========================================================================

@login_required
def vista_perfil(request):
    if request.method == "POST":              
        form = UsuarioEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.POST.get("eliminar_avatar") == "1":
                user.avatar.delete(save=False)
                user.avatar = "avatars/default.png"
            
            user.save()
            messages.success(request, "Perfil actualizado con éxito")
            return redirect("pagina_inicio")
    else:
        form = UsuarioEditForm(instance=request.user)
    
    return render(request, "usuarios/perfil.html", {"form": form})


