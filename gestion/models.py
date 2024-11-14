from django.db import models
from django.contrib.auth.models import User

class Empleado(models.Model):
    HORARIO_CHOICES = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('C', 'Completo'),
        ('O', 'Otros'),
    ]
    ACTIVO_CHOICES = [
        (True, 'SI'),
        (False, 'NO'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    activo = models.BooleanField(choices=ACTIVO_CHOICES, default=True)
    horario = models.CharField(max_length=1, choices=HORARIO_CHOICES, default='O')
    observaciones = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='empleados/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = 'empleados/default.jpg'  # Ruta dentro de la carpeta media/
        super(Empleado, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"


class Tarea(models.Model):
    CAMPAÑA_CHOICES = [
        ('BSL', 'BSL'),
        ('JUGUETES', 'Juguetes'),
        ('VIVAMOS', 'Vivamos Circular'),
        ('NINGUNO', 'Ninguno'),
    ]
    nombre = models.CharField(max_length=100)
    campaña = models.CharField(max_length=8, choices=CAMPAÑA_CHOICES, default='NINGUNO')
    imagen = models.ImageField(upload_to='tareas/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"


class Mesa(models.Model):
    numero = models.IntegerField()
    empleados = models.ManyToManyField(Empleado, blank=True)
    tareas = models.ManyToManyField(Tarea, blank=True)
    horario = models.CharField(max_length=1, choices=Empleado.HORARIO_CHOICES, default='M')
    jefe_mesa = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name='jefe_mesa')

    class Meta:
        unique_together = ('numero', 'horario')
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"

    def __str__(self):
        return f"Mesa {self.numero} - Horario {self.get_horario_display()}"


class PuestosDelDia(models.Model):
    HORARIO_CHOICES = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('C', 'Completo'),
    ]
    fecha = models.DateField()
    horario = models.CharField(max_length=1, choices=HORARIO_CHOICES)
    mesas = models.ManyToManyField(Mesa)
    comentario = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('fecha', 'horario')
        verbose_name = "Puesto del Día"
        verbose_name_plural = "Puestos del Día"

    def __str__(self):
        return f"Puestos del día {self.fecha} - {self.get_horario_display()}"


class RegistroActividad(models.Model):
    TURNOS = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('C', 'Completo')
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    turno = models.CharField(max_length=1, choices=TURNOS, default='M')

    def __str__(self):
        return f'{self.usuario.username} - {self.descripcion} ({self.fecha})'
