from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Ruta, Vehiculo, Conductor

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