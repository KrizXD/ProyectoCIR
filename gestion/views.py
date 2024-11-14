from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PuestosDelDia, Mesa, Empleado, Tarea, RegistroActividad
from .forms import EmpleadoForm, TareaForm
from django.db.models import Q
from datetime import datetime
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def home(request):
    # Obtener la fecha y la hora actual
    fecha_hora_actual = localtime(timezone.now())

    # Determinar el horario predeterminado (mañana o tarde según la hora actual)
    horario_default = 'M' if fecha_hora_actual.hour < 12 else 'T'

    # Verificar si el usuario es Fabian o Edgardo
    es_fabian = request.user.is_authenticated and request.user.username == 'fabi'
    es_edgardo = request.user.is_authenticated and request.user.username == 'edgardo'
    es_admin = es_fabian or es_edgardo

    # Si es Fabian o Edgardo, permitir cambiar el horario y guardar la selección en la sesión
    if es_admin:
        if 'horario' in request.POST:
            horario_actual = request.POST.get('horario')
            request.session['horario_actual'] = horario_actual  # Guardar en sesión
        else:
            horario_actual = request.session.get('horario_actual', horario_default)
    else:
        horario_actual = horario_default

    # Filtrar las mesas asignadas al horario correspondiente, junto con sus tareas y empleados
    mesas = Mesa.objects.filter(horario=horario_actual).prefetch_related('tareas', 'empleados')

    # Filtrar empleados asignados a mesas del horario correspondiente
    empleados_asignados = Empleado.objects.filter(mesa__horario=horario_actual).distinct()

    # Filtrar empleados activos con el horario seleccionado y aquellos con horario completo
    empleados_activos = Empleado.objects.filter(activo=True).filter(horario__in=[horario_actual, 'C']).exclude(id__in=empleados_asignados)

    return render(request, 'home.html', {
        'fecha_hora': fecha_hora_actual,
        'mesas': mesas,
        'empleados_activos': empleados_activos,
        'horario_actual': horario_actual,
        'es_fabian': es_fabian,
        'es_edgardo': es_edgardo,
    })


# Vista para gestionar todas las tareas (Agregar, quitar tareas a las mesas)
@login_required
def gestionar_todas_las_tareas(request):
    # Obtener todas las mesas y tareas disponibles
    mesas = Mesa.objects.all().prefetch_related('tareas')
    todas_las_tareas = Tarea.objects.all()

    if request.method == 'POST':
        # Verificar si se está agregando una tarea
        if 'agregar_tarea' in request.POST:
            mesa_id = request.POST.get('mesa_id')
            tarea_id = request.POST.get('tarea_id')
            mesa = get_object_or_404(Mesa, id=mesa_id)
            tarea = get_object_or_404(Tarea, id=tarea_id)
            mesa.tareas.add(tarea)
            # Registrar actividad
            RegistroActividad.objects.create(
                usuario=request.user,
                descripcion=f'{request.user.username} agregó la tarea {tarea.nombre} a la mesa {mesa.numero}.'
            )

        # Verificar si se está quitando una tarea
        elif 'quitar_tarea' in request.POST:
            tarea_id = request.POST.get('tarea_id')
            mesa_id = request.POST.get('mesa_id')
            mesa = get_object_or_404(Mesa, id=mesa_id)
            tarea = get_object_or_404(Tarea, id=tarea_id)
            mesa.tareas.remove(tarea)
            # Registrar actividad
            RegistroActividad.objects.create(
                usuario=request.user,
                descripcion=f'{request.user.username} quitó la tarea {tarea.nombre} de la mesa {mesa.numero}.'
            )

        # Redirigir nuevamente a la gestión de todas las tareas
        return redirect('gestionar_todas_las_tareas')

    return render(request, 'gestionar_tareas.html', {
        'mesas': mesas,
        'todas_las_tareas': todas_las_tareas
    })

# Vista para asignar empleados a mesas
@login_required
def asignar_empleado_a_mesa(request, mesa_id, empleado_id):
    if request.method == 'POST' and request.user.username in ['fabi', 'edgardo']:
        mesa = get_object_or_404(Mesa, id=mesa_id)
        empleado = get_object_or_404(Empleado, id=empleado_id)

        # Remover al empleado de cualquier otro mesón en el mismo horario antes de asignarlo
        mesas = Mesa.objects.filter(horario=mesa.horario)
        for m in mesas:
            if empleado in m.empleados.all():
                m.empleados.remove(empleado)

        # Asignar el empleado al nuevo mesón
        mesa.empleados.add(empleado)
        mesa.save()

        # Registrar actividad
        descripcion = f'{request.user.username} asignó al empleado {empleado.nombre} {empleado.apellido} a la mesa {mesa.numero}.'
        RegistroActividad.objects.create(usuario=request.user, descripcion=descripcion)

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=403)

# Vista para remover empleados de mesas
@login_required
def remover_empleado_de_mesa(request, empleado_id):
    if request.method == 'POST' and request.user.username in ['fabi', 'edgardo']:
        empleado = get_object_or_404(Empleado, id=empleado_id)

        # Remover al empleado de todas las mesas del mismo horario
        mesas = Mesa.objects.filter(horario=empleado.horario)
        for mesa in mesas:
            if empleado in mesa.empleados.all():
                mesa.empleados.remove(empleado)
                mesa.save()

        # Registrar actividad
        descripcion = f'{request.user.username} removió al empleado {empleado.nombre} {empleado.apellido} de todas las mesas del horario {empleado.horario}.'
        RegistroActividad.objects.create(usuario=request.user, descripcion=descripcion)

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=403)

# Vista para actualizar los puestos en tiempo real (usando AJAX)
def actualizar_puestos(request):
    horario = request.GET.get('horario')
    fecha_actual = timezone.now().date()

    # Filtrar los PuestosDelDia por la fecha actual y el horario seleccionado
    puesto = PuestosDelDia.objects.filter(fecha=fecha_actual, horario=horario).first()

    mesas_data = []
    if puesto:
        for mesa in puesto.mesas.all():
            mesas_data.append({
                'mesa': f'Mesa {mesa.numero}',
                'empleados': list(mesa.empleados.values('nombre', 'apellido')),
                'tareas': list(mesa.tareas.values('nombre'))
            })

    return JsonResponse({'mesas': mesas_data})

# Vista para editar un empleado
@login_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            # Registrar actividad
            RegistroActividad.objects.create(
                usuario=request.user,
                descripcion=f'{request.user.username} editó la información del empleado {empleado.nombre} {empleado.apellido}.'
            )
            return redirect('home')
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'editar_empleado.html', {'form': form, 'empleado': empleado})

# Vista para eliminar un empleado (solo Edgardo puede eliminar)
@login_required
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST' and request.user.username == 'edgardo':
        empleado.delete()
        # Registrar actividad
        RegistroActividad.objects.create(
            usuario=request.user,
            descripcion=f'{request.user.username} eliminó al empleado {empleado.nombre} {empleado.apellido}.'
        )
        return redirect('home')
    return JsonResponse({'status': 'error'}, status=403)

# Vista para agregar un nuevo empleado (solo Edgardo puede agregar)
@login_required
def agregar_empleado(request):
    if request.method == 'POST' and request.user.username == 'edgardo':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            empleado = form.save()
            # Registrar actividad
            RegistroActividad.objects.create(
                usuario=request.user,
                descripcion=f'{request.user.username} agregó al nuevo empleado {empleado.nombre} {empleado.apellido}.'
            )
            return redirect('home')
    else:
        form = EmpleadoForm()

    return render(request, 'agregar_empleado.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def ver_registro_actividades(request):
    registros = RegistroActividad.objects.all().order_by('-fecha')

    query = request.GET.get('q', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    turno = request.GET.get('turno', '')

    if query:
        registros = registros.filter(Q(usuario__username__icontains=query) | Q(descripcion__icontains=query))
    if fecha_inicio:
        registros = registros.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        registros = registros.filter(fecha__lte=fecha_fin)
    if turno:
        registros = registros.filter(turno=turno)

    paginator = Paginator(registros, 20)  # 20 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'turno': turno,
    }

    return render(request, 'ver_registro_actividades.html', context)


# Función para asignar empleados a una mesa
@login_required
def asignar_empleado_a_mesa(request, mesa_id, empleado_id):
    if request.method == 'POST' and request.user.username in ['fabi', 'edgardo']:
        mesa = get_object_or_404(Mesa, id=mesa_id)
        empleado = get_object_or_404(Empleado, id=empleado_id)

        # Remover al empleado de cualquier otro mesón en el mismo horario o en horario completo antes de asignarlo
        mesas = Mesa.objects.filter(horario__in=[mesa.horario, 'C'])
        for m in mesas:
            if empleado in m.empleados.all():
                m.empleados.remove(empleado)

        # Asignar el empleado al nuevo mesón
        mesa.empleados.add(empleado)

        # Registrar actividad
        descripcion = f'{request.user.username} asignó al empleado {empleado.nombre} {empleado.apellido} a la mesa {mesa.numero}.'
        RegistroActividad.objects.create(usuario=request.user, descripcion=descripcion)

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=403)

# Función para remover empleados de una mesa y moverlos a la lista de empleados activos
@login_required
def remover_empleado_de_mesa(request, empleado_id):
    if request.method == 'POST' and request.user.username in ['fabi', 'edgardo']:
        empleado = get_object_or_404(Empleado, id=empleado_id)

        # Remover al empleado de todas las mesas sin importar el horario
        mesas = Mesa.objects.filter(empleados=empleado)
        for mesa in mesas:
            mesa.empleados.remove(empleado)

        # Registrar actividad
        descripcion = f'{request.user.username} removió al empleado {empleado.nombre} {empleado.apellido} de todas las mesas.'
        RegistroActividad.objects.create(usuario=request.user, descripcion=descripcion)

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=403)


@login_required
def finalizar_turno(request, turno):
    if request.method == 'POST':
        # Obtén todas las mesas para el turno actual
        mesas = Mesa.objects.filter(horario=turno)
        disposiciones = []

        # Crear un texto con la disposición de cada mesa y sus empleados
        for mesa in mesas:
            empleados = ', '.join([f"{empleado.nombre} {empleado.apellido}" for empleado in mesa.empleados.all()])
            if empleados:
                disposicion = f"Mesa {mesa.numero}: {empleados}"
                disposiciones.append(disposicion)

        # Generar la descripción en formato texto
        descripcion = f"Disposición del turno {turno.upper()} finalizada por {request.user.username}:\n" + '\n'.join(disposiciones)
        
        # Registrar en RegistroActividad
        RegistroActividad.objects.create(
            usuario=request.user,
            descripcion=descripcion,
            fecha=timezone.now(),
            turno=turno
        )

        # Limpiar las mesas (vaciar empleados)
        for mesa in mesas:
            mesa.empleados.clear()

        # Responder con éxito y redireccionar a la página inicial
        return JsonResponse({"status": "ok", "message": "Turno finalizado y disposición guardada."})
    
    # Si no se usa POST, retornar error
    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)

@login_required
def descargar_registro_puestos(request, registro_id):
    # Obtener el registro específico basado en el ID
    registro = get_object_or_404(RegistroActividad, id=registro_id)
    
    # Construir el contenido del archivo de texto
    contenido = f"Registro de Actividades\n\n"
    contenido += f"Fecha: {registro.fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
    contenido += f"Usuario: {registro.usuario.username}\n"
    contenido += f"Turno: {registro.get_turno_display()}\n"
    contenido += "Disposición de los Mesones:\n"
    
    # Ordenar los mesones y separarlos por /
    mesas = registro.descripcion.split("Mesa ")
    mesas_ordenadas = sorted(mesas[1:], key=lambda x: int(x.split(":")[0]))
    for mesa in mesas_ordenadas:
        contenido += f"Mesa {mesa.strip()} / "  # Usamos el separador "/"

    # Crear y enviar el archivo de texto como respuesta
    response = HttpResponse(contenido, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="registro_{registro.fecha.strftime("%Y%m%d_%H%M%S")}.txt"'
    return response


def asignar_jefe_mesa(request, mesa_id, empleado_id):
    if request.method == 'POST':
        try:
            mesa = Mesa.objects.get(pk=mesa_id)
            empleado = Empleado.objects.get(pk=empleado_id)
            mesa.jefe_mesa = empleado  # Asume que tienes un campo jefe_mesa en el modelo Mesa
            mesa.save()
            return JsonResponse({'success': True})
        except Mesa.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mesa no encontrada'})
        except Empleado.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Empleado no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def quitar_jefe_mesa(request, mesa_id, empleado_id):
    if request.method == 'POST':
        try:
            mesa = Mesa.objects.get(pk=mesa_id)
            empleado = Empleado.objects.get(pk=empleado_id)
            if mesa.jefe_mesa == empleado:
                mesa.jefe_mesa = None
                mesa.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'El empleado no es el jefe de esta mesa.'})
        except Mesa.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mesa no encontrada.'})
        except Empleado.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Empleado no encontrado.'})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})