function mostrarDiaYFecha() {
    const opcionesDia = { weekday: 'long' };
    const opcionesFecha = { year: 'numeric', month: '2-digit', day: '2-digit' };
    
    const hoy = new Date();
    const diaSemana = hoy.toLocaleDateString('es-ES', opcionesDia);
    const fechaNumerica = hoy.toLocaleDateString('es-ES', opcionesFecha);
    
    // Mostrar el día de la semana en el elemento con id 'titulo-dia'
    const tituloDia = document.getElementById('titulo-dia');
    if (tituloDia) {
        tituloDia.textContent = diaSemana.charAt(0).toUpperCase() + diaSemana.slice(1);
    }
    
    // Mostrar la fecha completa en el elemento con id 'fecha-completa'
    const fechaCompleta = document.getElementById('fecha-completa');
    if (fechaCompleta) {
        fechaCompleta.textContent = fechaNumerica;
    }
}

// Ejecutar la función al cargar la página
window.onload = function() {
    mostrarDiaYFecha();
};
