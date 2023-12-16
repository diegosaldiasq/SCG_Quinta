document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var nombrePersonal = $("#nombre-personal").val();
            var turno = $("#turno").val();
            var planta = $("#planta").val();
            var area = $("#area").val();
            var cumplimiento = $("#cumpl").val();
            var desviacion = $("#desv").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();
            var observacion = $("#obs").val();

            // agregar valores a datos

            var datos = {
                nombre_personal: nombrePersonal,
                turno: turno,
                planta: planta,
                area: area,
                cumplimiento: cumplimiento,
                desviacion: desviacion,
                accion_correctiva: accionCorrectiva,
                verificacion_accion_correctiva: verificacionAccionCorrectiva,
                observacion: observacion
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/higiene_y_conducta_personal/vista_higiene_y_conducta_personal/', {
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
