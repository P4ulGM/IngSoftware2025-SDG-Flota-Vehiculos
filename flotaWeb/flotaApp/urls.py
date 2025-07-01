from django.urls import path
from .views import home, register, nosotros, asignar_ruta, ver_ruta, emitir_reporte, hacer_mantencion

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('nosotros/', nosotros , name='nosotros'),
    path('asignar_ruta/', asignar_ruta, name='asignar_ruta'),
    path('ver_ruta/', ver_ruta, name='ver_ruta'),
    path('emitir_reporte/', emitir_reporte, name='emitir_reporte'),
    path('hacer_mantencion/', hacer_mantencion, name='hacer_mantencion'),
]