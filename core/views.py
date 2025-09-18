from django.shortcuts import render, redirect
from core.models import Usuario
from core.forms import RegistroForm
from django.contrib import messages

# Create your views here.

def crear_usuario(request):
    if request.method == "POST":
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario registrado con éxito.")
            formulario = RegistroForm()
    else:
        formulario = RegistroForm()

    return render(request, "core/usuarios/usuario_form.html", {"form": formulario})