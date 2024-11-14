from django.contrib import admin
from .models import Empleado, Tarea, Mesa, PuestosDelDia

admin.site.register(Empleado)
admin.site.register(Tarea)
admin.site.register(Mesa)
admin.site.register(PuestosDelDia)
