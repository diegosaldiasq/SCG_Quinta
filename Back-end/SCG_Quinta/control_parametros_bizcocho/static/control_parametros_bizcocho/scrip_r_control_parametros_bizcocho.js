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
            // obtener valores de los campos
            var cliente = document.getElementById("cliente").value;
            var codigoProducto = document.getElementById("codigo-producto").value;
            var producto = document.getElementById("producto").value;
            var velocidadBomba = parseInt(document.getElementById("velocidad-bomba").value);
            var velocidadTurbo = parseInt(document.getElementById("velocidad-turbo").value);
            var contrapresion = parseFloat(document.getElementById("contrapresion").value);
            var inyeccionAire = parseFloat(document.getElementById("inyeccion-aire").value);
            var densidad = parseFloat(document.getElementById("densidad").value);
            var temperaturaFinal = parseFloat(document.getElementById("t-final").value);
            var lote = document.getElementById("lote").value;
            var turno = document.getElementById("turno").value;

            // Nuevos campos para cantidad de agua y huevo
            var cantidadAgua = parseFloat(document.getElementById("cantidad-agua").value);
            var cantidadHuevo = parseFloat(document.getElementById("cantidad-huevo").value);

            // Validar que los nuevos campos no estén vacíos ni sean negativos
            if (isNaN(cantidadAgua) || cantidadAgua < 0) {
                alert("Por favor, ingresa una cantidad válida de agua (no negativa).");
                return;
            }
            if (isNaN(cantidadHuevo) || cantidadHuevo < 0) {
                alert("Por favor, ingresa una cantidad válida de huevo (no negativa).");
                return;
            }

            // agregar valores a datos

            var datos = {
                cliente: cliente,
                codigo_producto: codigoProducto,
                producto: producto,
                cantidad_agua: cantidadAgua, // Nuevo campo
                cantidad_huevo: cantidadHuevo, // Nuevo campo
                velocidad_bomba: velocidadBomba,
                velocidad_turbo: velocidadTurbo,
                contrapresion: contrapresion,
                inyeccion_aire: inyeccionAire,
                densidad: densidad,
                temperatura_final: temperaturaFinal,
                lote: lote,
                turno: turno
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/control_parametros_bizcocho/vista_control_parametros_bizcocho/', {
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
                //alert("No se pudo guardar... revisa nuevamente!!");
                //return false;
                const mensajeError = data.error ? `Error del servidor: ${data.error}` : "No se pudo guardar... revisa nuevamente!!";
                console.error("Respuesta del servidor:", data);
                alert(mensajeError);
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al cargar los datos, formatos no coinciden!!");
        }
    });
});