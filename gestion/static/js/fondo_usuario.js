window.onload = function() {
    // Reemplaza {{ request.user.username }} con una variable de contexto si es necesario
    let user = window.username || "default_user"; // Usa "default_user" o ajusta según necesites

    // Obtener el fondo guardado del almacenamiento local
    const fondoGuardado = localStorage.getItem('fondo_' + user);
    if (fondoGuardado) {
        document.body.style.background = fondoGuardado;
    } else {
        // Si no hay fondo guardado, establece un fondo predeterminado si no son Fabián o Edgardo
        if (typeof esFabian === "undefined" || typeof esEdgardo === "undefined" || (!esFabian && !esEdgardo)) {
            document.body.style.backgroundColor = 'gray'; 
        }
    }
};

function cambiarFondoColor(color) {
    let user = window.username || "default_user"; // Usa "default_user" o ajusta según necesites
    document.body.style.backgroundColor = color;
    document.body.style.backgroundImage = 'none'; 
    localStorage.setItem('fondo_' + user, color); 
}

function cambiarFondoImagen(input) {
    let user = window.username || "default_user"; // Usa "default_user" o ajusta según necesites
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.body.style.backgroundImage = 'url(' + e.target.result + ')';
            localStorage.setItem('fondo_' + user, 'url(' + e.target.result + ')');
        };
        reader.readAsDataURL(file);
    }
}

function toggleOpcionesFondo() {
    const opcionesFondo = document.getElementById('opciones-fondo');
    opcionesFondo.style.display = opcionesFondo.style.display === 'none' ? 'block' : 'none';
}
