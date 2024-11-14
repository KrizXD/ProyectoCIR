from django.urls import path
from django.contrib import admin
from gestion import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),

    # Ruta para la página principal (home)
    path('', views.home, name='home'),

    # Ruta para el inicio de sesión utilizando vistas genéricas de Django
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Ruta para el cierre de sesión, que redirige a la página principal después de cerrar sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Ruta para asignar empleados a mesas
    path('asignar_empleado_a_mesa/<int:mesa_id>/<int:empleado_id>/', views.asignar_empleado_a_mesa, name='asignar_empleado_a_mesa'),

    # Ruta para remover empleados de mesas
    path('remover_empleado_de_mesa/<int:empleado_id>/', views.remover_empleado_de_mesa, name='remover_empleado_de_mesa'),
    
    path('editar_empleado/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    
    path('agregar-empleado/', views.agregar_empleado, name='agregar_empleado'),
    
    path('gestionar-tareas/', views.gestionar_todas_las_tareas, name='gestionar_todas_las_tareas'),
    
    path('ver-registro-actividades/', views.ver_registro_actividades, name='ver_registro_actividades'),
    
    path('finalizar-turno/<str:turno>/', views.finalizar_turno, name='finalizar_turno'),

    path('descargar-registro-puestos/<int:registro_id>/', views.descargar_registro_puestos, name='descargar_registro_puestos'),
    
    path('asignar_jefe_mesa/<int:mesa_id>/<int:empleado_id>/', views.asignar_jefe_mesa, name='asignar_jefe_mesa'),
    
    path('quitar_jefe_mesa/<int:mesa_id>/<int:empleado_id>/', views.quitar_jefe_mesa, name='quitar_jefe_mesa'),


]

# Añadir configuración para servir archivos de medios en modo desarrollo (como imágenes)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
