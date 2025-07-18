# Generated by Django 5.2.1 on 2025-07-01 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flotaApp', '0002_conductor_vehiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(max_length=255, verbose_name='Origen')),
                ('destino', models.CharField(max_length=255, verbose_name='Destino')),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Asignación')),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Inicio')),
                ('fecha_fin', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Fin')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('EN_CURSO', 'En Curso'), ('COMPLETADA', 'Completada'), ('CANCELADA', 'Cancelada')], default='PENDIENTE', max_length=15, verbose_name='Estado')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('conductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flotaApp.conductor', verbose_name='Conductor')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flotaApp.vehiculo', verbose_name='Vehículo')),
            ],
            options={
                'verbose_name': 'Ruta',
                'verbose_name_plural': 'Rutas',
                'ordering': ['-fecha_asignacion'],
            },
        ),
    ]
