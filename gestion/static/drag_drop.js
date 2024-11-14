// Función para obtener el token CSRF de las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Permitir el evento drop en los elementos válidos
function allowDrop(ev) {
    ev.preventDefault();
}

// Función que se activa al empezar a arrastrar un elemento
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);  // Almacena el ID del empleado arrastrado
}

// Función para mostrar/ocultar el placeholder según el número de empleados en la lista
function actualizarPlaceholder() {
    const empleadosList = document.getElementById('empleados-list');
    const dropPlaceholder = document.getElementById('drop-placeholder');

    // Si hay empleados en la lista, ocultar el placeholder
    if (empleadosList.children.length > 1) {  // Hay más de 1 elemento, que puede incluir el placeholder
        dropPlaceholder.style.display = 'none';
    } else {
        // Si no hay empleados, mostrar el placeholder
        dropPlaceholder.style.display = 'block';
    }
}

// Función que se activa cuando un empleado es soltado en un área permitida
function drop(ev) {
    ev.preventDefault();
    
    var data = ev.dataTransfer.getData("text");  // ID del empleado arrastrado
    var empleadoElement = document.getElementById(data);  // Elemento del empleado arrastrado
    
    // Verifica si el contenedor donde se suelta es una mesa o la lista de empleados
    if (ev.target.classList.contains('mesa') || ev.target.closest('.mesa')) {
        // Si se suelta en una mesa
        var mesaElement = ev.target.closest('.mesa');
        var mesaId = mesaElement.id.split('-')[1];  // Extrae el ID de la mesa desde el ID del elemento
        var empleadoId = data.split('-')[1];  // Extrae el ID del empleado
        
        // Mueve el empleado al contenedor de la mesa
        document.getElementById('empleados-mesa-' + mesaId).appendChild(empleadoElement);
        
        // Enviar solicitud AJAX para actualizar la asignación en el backend
        fetch(`/asignar_empleado_a_mesa/${mesaId}/${empleadoId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (!response.ok) {
                alert('Error al asignar empleado.');
            }
        });
        
        // Actualizar el placeholder
        actualizarPlaceholder();
        
    } else if (ev.target.id === 'empleados-list' || ev.target.closest('#empleados-list')) {
        // Si se suelta en la lista de empleados (para remover del mesón y regresar a empleados activos)
        var empleadoId = data.split('-')[1];  // Extrae el ID del empleado
        
        // Mueve el empleado de vuelta a la lista de empleados activos
        document.getElementById('empleados-list').appendChild(empleadoElement);
        
        // Enviar solicitud AJAX para desasignar al empleado de cualquier mesa
        fetch(`/remover_empleado_de_mesa/${empleadoId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (!response.ok) {
                alert('Error al remover empleado del mesón.');
            }
        });

        // Actualizar el placeholder
        actualizarPlaceholder();
    }
}
