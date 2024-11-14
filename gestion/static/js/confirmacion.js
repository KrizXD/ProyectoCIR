function mostrarConfirmacion() {
    const modal = document.getElementById("modalConfirmacion");
    modal.style.display = "block";
}

function cerrarConfirmacion() {
    const modal = document.getElementById("modalConfirmacion");
    modal.style.display = "none";
}

function confirmarFinalizarTurno() {
    const turnoActual = document.querySelector('select[name="horario"]').value;
    const url = `/finalizar-turno/${turnoActual}/`;

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            alert(data.message);
            window.location.reload();
        } else {
            alert("Hubo un problema al finalizar el turno: " + data.message);
        }
    })
    .catch(error => {
        alert("Error en la solicitud. Inténtalo de nuevo.");
        console.error("Error:", error);
    });
}
