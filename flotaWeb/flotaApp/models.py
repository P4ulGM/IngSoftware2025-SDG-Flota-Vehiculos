from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Logistico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Logístico"
        verbose_name_plural = "Logísticos"


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"


class Jefe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Jefe"
        verbose_name_plural = "Jefes"


class Vehiculo(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('NO_DISPONIBLE', 'No Disponible'),
    ]
    
    patente = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Patente"
    )
    marca = models.CharField(
        max_length=50,
        verbose_name="Marca"
    )
    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo"
    )
    año = models.IntegerField(
        verbose_name="Año"
    )
    kilometraje = models.IntegerField(
        default=0,
        verbose_name="Kilometraje"
    )
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE',
        verbose_name="Estado"
    )
    
    def __str__(self):
        return f"{self.patente} - {self.marca} {self.modelo}"
    
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['patente']


class Conductor(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('NO_DISPONIBLE', 'No Disponible'),
    ]
    
    nombre = models.CharField(
        max_length=50,
        verbose_name="Nombre"
    )
    apellido = models.CharField(
        max_length=50,
        verbose_name="Apellido"
    )
    rut = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="RUT"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    documentos = models.TextField(
        blank=True,
        null=True,
        verbose_name="Documentos"
    )
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE',
        verbose_name="Estado"
    )
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"
    
    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"
        ordering = ['apellido', 'nombre']


class Ruta(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_CURSO', 'En Curso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        verbose_name="Vehículo"
    )
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
        verbose_name="Conductor"
    )
    origen = models.CharField(
        max_length=255,
        verbose_name="Origen"
    )
    destino = models.CharField(
        max_length=255,
        verbose_name="Destino"
    )
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Asignación"
    )
    fecha_inicio = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de Inicio"
    )
    fecha_fin = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de Fin"
    )
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado"
    )

    def __str__(self):
        return f"Ruta {self.id}: {self.origen} → {self.destino} ({self.vehiculo.patente})"
    
    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"
        ordering = ['-fecha_asignacion']


class Mantencion(models.Model):
    TIPO_CHOICES = [
        ('PREVENTIVO', 'Mantenimiento Preventivo'),
        ('CORRECTIVO', 'Mantenimiento Correctivo'),
        ('REVISION_TECNICA', 'Revisión Técnica'),
        ('CAMBIO_ACEITE', 'Cambio de Aceite'),
        ('CAMBIO_NEUMATICOS', 'Cambio de Neumáticos'),
        ('CAMBIO_FRENOS', 'Cambio de Frenos'),
        ('REPARACION_MOTOR', 'Reparación de Motor'),
        ('REPARACION_TRANSMISION', 'Reparación de Transmisión'),
        ('OTROS', 'Otros'),
    ]
    
    ESTADO_CHOICES = [
        ('PROGRAMADO', 'Programado'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        verbose_name="Vehículo"
    )
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
        verbose_name="Conductor Responsable"
    )
    fecha_hora = models.DateTimeField(
        verbose_name="Fecha y Hora"
    )
    tipo_mantenimiento = models.CharField(
        max_length=25,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Mantenimiento"
    )
    taller = models.CharField(
        max_length=255,
        verbose_name="Taller"
    )
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Costo (CLP)"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción Detallada"
    )
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='PROGRAMADO',
        verbose_name="Estado"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )
    
    def __str__(self):
        return f"{self.get_tipo_mantenimiento_display()} - {self.vehiculo.patente} ({self.fecha_hora.strftime('%d/%m/%Y')})"
    
    class Meta:
        verbose_name = "Mantención"
        verbose_name_plural = "Mantenciones"
        ordering = ['-fecha_hora']
