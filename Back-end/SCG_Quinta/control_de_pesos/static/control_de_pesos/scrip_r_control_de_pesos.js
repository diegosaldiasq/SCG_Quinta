// Configuración global de jQuery para incluir CSRF en todas las peticiones POST/AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
     // 1) Restaurar lote y turno guardados en sessionStorage
    const loteGuardado  = sessionStorage.getItem('lote');
    const turnoGuardado = sessionStorage.getItem('turno');

    if (loteGuardado !== null) {
        document.getElementById('lote').value = loteGuardado;
        sessionStorage.removeItem('lote');
    }
    if (turnoGuardado !== null) {
        document.getElementById('turno').value = turnoGuardado;
        sessionStorage.removeItem('turno');
    }

    // 2) Listener para el botón
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var cliente = $("#cliente").val();
            var codigoProducto = $("#codigo").val();
            var producto = $("#producto").val();
            var pesoReceta = $("#peso").val();
            var pesoReal = $("#peso-real").val();
            var lote = $("#lote").val();
            var turno = $("#turno").val();

            // agregar valores a datos

            var datos = {
                cliente: cliente,
                producto: producto,
                codigo_producto: codigoProducto,
                peso_receta: pesoReceta,
                peso_real: pesoReal,
                lote: lote,
                turno: turno
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/control_de_pesos/vista_control_de_pesos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
                },
                body: JSON.stringify({ dato: datos })
            });
            var data = await response.json();
            debugger; // <-- Agrega esta línea
            if (data.existe) {
                 // guardamos lote y turno en sessionStorage
                sessionStorage.setItem('lote', lote);
                sessionStorage.setItem('turno', turno);

                alert("Datos guardados exitosamente!!");
                location.reload();
            } else {
                alert("No se pudo guardar... revisa nuevamente!!");
                return false;
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al cargar los datos, formatos no coinciden!!");
        }
    });
});