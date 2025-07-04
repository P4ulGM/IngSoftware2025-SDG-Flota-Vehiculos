from .models import Notificacion

def notificaciones(request):
    if request.user.is_authenticated:
        count = Notificacion.objects.filter(usuario=request.user, leido=False).count()
    else:
        count = 0
    return {'notificaciones_no_leidas': count}
