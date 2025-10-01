from usuarios.models import Usuario


def obtener_usuario(request):
    usuario_id = request.session.get("usuario_id")
    return Usuario.objects.get(id=usuario_id)
    