document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var lote = $("#lote").val();
            var turno = $("#turno").val();
            var tipoMetal = $("#tipo-metal").val();
            var medicion = $("#medicion").val();
            var producto =  $("#producto").val();
            var observaciones = $("#obs").val();
            var accionCorrectiva = $("#ac").val();

            // agregar valores a datos

            var datos = {
                lote: lote,
                turno: turno,
                tipo_metal: tipoMetal,
                medicion: medicion,
                producto: producto,
                observaciones: observaciones,
                accion_correctiva: accionCorrectiva
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/pcc2_detector_metales/vista_pcc2_detector_metales/', {
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