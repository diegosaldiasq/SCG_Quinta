document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var numeroDeEstacion = $("#numero-estacion").val();
            var tipoDePlaga = $("#tipo-plaga").val();
            var tipoDeTrampa = $("#tipo-trampa").val();
            var ubicacion = $("#ubicacion").val();
            var monitoreo = $("#monitoreo").val();
            var accionCorrectiva = $("#ac").val();

            // agregar valores a datos

            var datos = {
                numero_estacion: numeroDeEstacion,
                tipo_plaga: tipoDePlaga,
                tipo_trampa: tipoDeTrampa,
                ubicacion: ubicacion,
                monitoreo: monitoreo,
                accion_correctiva: accionCorrectiva
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/monitoreo_de_plagas/vista_monitoreo_de_plagas/', {
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