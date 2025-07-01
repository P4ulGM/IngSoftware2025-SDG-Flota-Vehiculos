from django.contrib import admin
from .models import Logistico, Supervisor, Jefe, Vehiculo, Conductor, Ruta

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
