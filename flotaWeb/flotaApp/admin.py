from django.contrib import admin
from .models import Logistico, Supervisor, Jefe, Vehiculo, Conductor, Ruta, Mantencion

# Register your models here.
admin.site.register(Logistico)
admin.site.register(Supervisor)
admin.site.register(Jefe)
admin.site.register(Vehiculo)
admin.site.register(Conductor)

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'conductor', 'origen', 'destino', 'estado', 'fecha_asignacion')
    list_filter = ('estado', 'fecha_asignacion', 'vehiculo', 'conductor')
    search_fields = ('origen', 'destino', 'vehiculo__patente', 'conductor__nombre', 'conductor__apellido')
    readonly_fields = ('fecha_asignacion',)
    date_hierarchy = 'fecha_asignacion'

@admin.register(Mantencion)
class MantencionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'conductor', 'tipo_mantenimiento', 'taller', 'costo', 'fecha_hora', 'estado')
    list_filter = ('estado', 'tipo_mantenimiento', 'fecha_hora', 'vehiculo', 'taller')
    search_fields = ('vehiculo__patente', 'conductor__nombre', 'conductor__apellido', 'taller', 'descripcion')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    date_hierarchy = 'fecha_hora'
    ordering = ('-fecha_hora',)
