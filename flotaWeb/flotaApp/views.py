from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, AsignarRutaForm, RegistrarMantencionForm, GenerarReporteForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Ruta, Vehiculo, Conductor, Mantencion, Supervisor, Notificacion
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone

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
            for supervisor in Supervisor.objects.all():
                Notificacion.objects.create(
                    usuario=supervisor.user,
                    mensaje=f"Nueva ruta asignada a {ruta.conductor.nombre} {ruta.conductor.apellido}"
                )
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
    rutas = Ruta.objects.all().order_by('-fecha_asignacion')
    context = {
        'rutas': rutas
    }
    return render(request, 'app/ver_ruta.html', context)

def emitir_reporte(request):
    if request.method == 'POST':
        form = GenerarReporteForm(request.POST)
        if form.is_valid():
            return generar_pdf_reporte(request, form.cleaned_data)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = GenerarReporteForm()
    
    context = {
        'form': form
    }
    return render(request, 'app/emitir_reporte.html', context)


def generar_pdf_reporte(request, data):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
    from io import BytesIO
    import locale
    
    # Configurar locale para formato de moneda
    try:
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        except:
            pass
    
    # Crear el objeto HttpResponse con cabeceras PDF
    response = HttpResponse(content_type='application/pdf')
    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="reporte_flota_{fecha_actual}.pdf"'
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    # Título del reporte
    titulo = f"Reporte de Flota - {data['tipo_reporte'].replace('_', ' ').title()}"
    elements.append(Paragraph(titulo, title_style))
    
    # Información del período
    periodo_info = f"Período: {data['fecha_inicio'].strftime('%d/%m/%Y')} - {data['fecha_fin'].strftime('%d/%m/%Y')}"
    elements.append(Paragraph(periodo_info, styles['Normal']))
    elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Filtros de fecha para las consultas
    fecha_inicio = timezone.make_aware(datetime.combine(data['fecha_inicio'], datetime.min.time()))
    fecha_fin = timezone.make_aware(datetime.combine(data['fecha_fin'], datetime.max.time()))
    
    # Generar contenido según el tipo de reporte
    tipo_reporte = data['tipo_reporte']
    
    if tipo_reporte in ['COMPLETO', 'VEHICULOS']:
        elements.append(Paragraph("VEHÍCULOS REGISTRADOS", heading_style))
        vehiculos = Vehiculo.objects.all()
        
        if vehiculos.exists():
            vehiculos_data = [['Patente', 'Marca', 'Modelo', 'Año', 'Estado', 'Kilometraje']]
            for vehiculo in vehiculos:
                vehiculos_data.append([
                    vehiculo.patente,
                    vehiculo.marca,
                    vehiculo.modelo,
                    str(vehiculo.año),
                    vehiculo.get_estado_display(),
                    f"{vehiculo.kilometraje:,} km"
                ])
            
            vehiculos_table = Table(vehiculos_data)
            vehiculos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(vehiculos_table)
        else:
            elements.append(Paragraph("No hay vehículos registrados.", styles['Normal']))
        
        elements.append(Spacer(1, 20))
    
    if tipo_reporte in ['COMPLETO', 'CONDUCTORES']:
        elements.append(Paragraph("CONDUCTORES REGISTRADOS", heading_style))
        conductores = Conductor.objects.all()
        
        if conductores.exists():
            conductores_data = [['Nombre', 'RUT', 'Email', 'Estado']]
            for conductor in conductores:
                conductores_data.append([
                    f"{conductor.nombre} {conductor.apellido}",
                    conductor.rut,
                    conductor.email,
                    conductor.get_estado_display()
                ])
            
            conductores_table = Table(conductores_data)
            conductores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(conductores_table)
        else:
            elements.append(Paragraph("No hay conductores registrados.", styles['Normal']))
        
        elements.append(Spacer(1, 20))
    
    if tipo_reporte in ['COMPLETO', 'RUTAS']:
        elements.append(Paragraph("RUTAS EN EL PERÍODO", heading_style))
        rutas = Ruta.objects.filter(
            fecha_asignacion__range=[fecha_inicio, fecha_fin]
        ).order_by('-fecha_asignacion')
        
        if rutas.exists():
            rutas_data = [['Fecha', 'Vehículo', 'Conductor', 'Origen', 'Destino', 'Estado']]
            for ruta in rutas:
                rutas_data.append([
                    ruta.fecha_asignacion.strftime('%d/%m/%Y'),
                    ruta.vehiculo.patente,
                    f"{ruta.conductor.nombre} {ruta.conductor.apellido}",
                    ruta.origen[:30] + "..." if len(ruta.origen) > 30 else ruta.origen,
                    ruta.destino[:30] + "..." if len(ruta.destino) > 30 else ruta.destino,
                    ruta.get_estado_display()
                ])
            
            rutas_table = Table(rutas_data)
            rutas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(rutas_table)
            
            # Estadísticas de rutas
            elements.append(Spacer(1, 10))
            total_rutas = rutas.count()
            pendientes = rutas.filter(estado='PENDIENTE').count()
            en_curso = rutas.filter(estado='EN_CURSO').count()
            completadas = rutas.filter(estado='COMPLETADA').count()
            
            stats_text = f"Total de rutas: {total_rutas} | Pendientes: {pendientes} | En curso: {en_curso} | Completadas: {completadas}"
            elements.append(Paragraph(stats_text, styles['Normal']))
        else:
            elements.append(Paragraph("No hay rutas registradas en el período seleccionado.", styles['Normal']))
        
        elements.append(Spacer(1, 20))
    
    if tipo_reporte in ['COMPLETO', 'MANTENCIONES']:
        elements.append(Paragraph("MANTENCIONES EN EL PERÍODO", heading_style))
        mantenciones = Mantencion.objects.filter(
            fecha_hora__range=[fecha_inicio, fecha_fin]
        ).order_by('-fecha_hora')
        
        if mantenciones.exists():
            mantenciones_data = [['Fecha', 'Vehículo', 'Tipo', 'Taller', 'Costo', 'Estado']]
            total_costo = 0
            
            for mantencion in mantenciones:
                mantenciones_data.append([
                    mantencion.fecha_hora.strftime('%d/%m/%Y'),
                    mantencion.vehiculo.patente,
                    mantencion.get_tipo_mantenimiento_display(),
                    mantencion.taller[:20] + "..." if len(mantencion.taller) > 20 else mantencion.taller,
                    f"${mantencion.costo:,.0f}",
                    mantencion.get_estado_display()
                ])
                total_costo += mantencion.costo
            
            mantenciones_table = Table(mantenciones_data)
            mantenciones_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(mantenciones_table)
            
            # Resumen de costos
            elements.append(Spacer(1, 10))
            resumen_text = f"Total de mantenciones: {mantenciones.count()} | Costo total: ${total_costo:,.0f}"
            elements.append(Paragraph(resumen_text, styles['Normal']))
        else:
            elements.append(Paragraph("No hay mantenciones registradas en el período seleccionado.", styles['Normal']))
    
    # Pie de página
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("---", styles['Normal']))
    elements.append(Paragraph("Sistema de Gestión de Flota Vehicular", styles['Normal']))
    
    # Generar el PDF
    doc.build(elements)
    
    return response

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


def notificaciones(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        notif_id = request.POST.get('marcar_leida')
        if notif_id:
            Notificacion.objects.filter(id=notif_id, usuario=request.user).update(leido=True)
            return redirect('notificaciones')

    notifs = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'app/notificaciones.html', {'notificaciones': notifs})


def dashboard(request):
    """Vista simple para mostrar un dashboard con conteos básicos."""
    vehiculos_count = Vehiculo.objects.count()
    conductores_count = Conductor.objects.count()
    pendientes = Ruta.objects.filter(estado='PENDIENTE').count()
    en_curso = Ruta.objects.filter(estado='EN_CURSO').count()
    completadas = Ruta.objects.filter(estado='COMPLETADA').count()

    vehiculos_disponibles = Vehiculo.objects.filter(estado='DISPONIBLE').count()
    vehiculos_no_disponibles = Vehiculo.objects.filter(estado='NO_DISPONIBLE').count()

    ultimas_rutas = Ruta.objects.all().order_by('-fecha_asignacion')[:5]
    ultimas_mantenciones = Mantencion.objects.all().order_by('-fecha_hora')[:5]

    context = {
        'vehiculos_count': vehiculos_count,
        'conductores_count': conductores_count,
        'pendientes': pendientes,
        'en_curso': en_curso,
        'completadas': completadas,
        'vehiculos_disponibles': vehiculos_disponibles,
        'vehiculos_no_disponibles': vehiculos_no_disponibles,
        'ultimas_rutas': ultimas_rutas,
        'ultimas_mantenciones': ultimas_mantenciones,
    }
    return render(request, 'app/dashboard.html', context)
