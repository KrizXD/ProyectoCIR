# Generated by Django 5.1.1 on 2024-10-08 17:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('activo', models.BooleanField(choices=[(True, 'SI'), (False, 'NO')], default=True)),
                ('horario', models.CharField(choices=[('M', 'Mañana'), ('T', 'Tarde'), ('C', 'Completo'), ('O', 'Otros')], default='O', max_length=1)),
                ('observaciones', models.TextField(blank=True)),
                ('imagen', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='empleados/')),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('campaña', models.CharField(choices=[('BSL', 'BSL'), ('JUGUETES', 'Juguetes'), ('VIVAMOS', 'Vivamos Circular'), ('NINGUNO', 'Ninguno')], default='NINGUNO', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(unique=True)),
                ('empleados', models.ManyToManyField(blank=True, to='gestion.empleado')),
                ('tareas', models.ManyToManyField(blank=True, to='gestion.tarea')),
            ],
        ),
        migrations.CreateModel(
            name='PuestosDelDia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('horario', models.CharField(choices=[('M', 'Mañana'), ('T', 'Tarde'), ('C', 'Completo')], max_length=1)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('mesas', models.ManyToManyField(to='gestion.mesa')),
            ],
            options={
                'unique_together': {('fecha', 'horario')},
            },
        ),
    ]
