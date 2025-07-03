from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, AsignarRutaForm, RegistrarMantencionForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)

def nosotros(request):
    return render(request, 'app/nosotros.html')

def asignar_ruta(request):
    if request.method == 'POST':
        form = AsignarRutaForm(request.POST)
        if form.is_valid():
            ruta = form.save()
            messages.success(request, f'Ruta asignada exitosamente: {ruta.origen} → {ruta.destino}')
            return redirect('asignar_ruta')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AsignarRutaForm()
    
    context = {
        'form': form
    }
    return render(request, 'app/asignar_ruta.html', context)

def ver_ruta(request):
    return render(request, 'app/ver_ruta.html')

def emitir_reporte(request):
    return render(request, 'app/emitir_reporte.html')

def hacer_mantencion(request):
    if request.method == 'POST':
        form = RegistrarMantencionForm(request.POST)
        if form.is_valid():
            mantencion = form.save()
            messages.success(request, f'Mantención registrada exitosamente para el vehículo {mantencion.vehiculo.patente}')
            return redirect('hacer_mantencion')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistrarMantencionForm()
    
    context = {
        'form': form
    }
    return render(request, 'app/hacer_mantencion.html', context)