from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Ruta, Vehiculo, Conductor, Mantencion

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email


class AsignarRutaForm(ModelForm):
    class Meta:
        model = Ruta
        fields = ['vehiculo', 'conductor', 'origen', 'destino']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'conductor': forms.Select(attrs={'class': 'form-control'}),
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de origen'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de destino'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo vehículos disponibles
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(estado='DISPONIBLE')
        # Filtrar solo conductores disponibles
        self.fields['conductor'].queryset = Conductor.objects.filter(estado='DISPONIBLE')
        
        # Agregar clases CSS y hacer campos requeridos más claros
        self.fields['vehiculo'].empty_label = "Seleccionar vehículo"
        self.fields['conductor'].empty_label = "Seleccionar conductor"
    
    def clean(self):
        cleaned_data = super().clean()
        vehiculo = cleaned_data.get('vehiculo')
        conductor = cleaned_data.get('conductor')
        
        # Validar que el vehículo esté disponible
        if vehiculo and vehiculo.estado != 'DISPONIBLE':
            raise forms.ValidationError('El vehículo seleccionado no está disponible.')
        
        # Validar que el conductor esté disponible
        if conductor and conductor.estado != 'DISPONIBLE':
            raise forms.ValidationError('El conductor seleccionado no está disponible.')
        
        return cleaned_data


class RegistrarMantencionForm(ModelForm):
    class Meta:
        model = Mantencion
        fields = ['vehiculo', 'conductor', 'fecha_hora', 'tipo_mantenimiento', 'taller', 'costo', 'descripcion']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'conductor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_hora': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'tipo_mantenimiento': forms.Select(attrs={'class': 'form-control'}),
            'taller': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del taller o mecánico'
            }),
            'costo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'step': '0.01',
                'min': '0'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa los detalles del mantenimiento a realizar...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar etiquetas vacías para los select
        self.fields['vehiculo'].empty_label = "Seleccionar vehículo"
        self.fields['conductor'].empty_label = "Seleccionar conductor"
        self.fields['tipo_mantenimiento'].empty_label = "Seleccionar tipo de mantenimiento"
        
        # Hacer que la descripción no sea obligatoria en el formulario
        self.fields['descripcion'].required = False
    
    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        if costo is not None and costo < 0:
            raise forms.ValidationError('El costo no puede ser negativo.')
        return costo
    
    def clean_fecha_hora(self):
        from django.utils import timezone
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if fecha_hora and fecha_hora < timezone.now():
            raise forms.ValidationError('La fecha y hora no puede ser en el pasado.')
        return fecha_hora