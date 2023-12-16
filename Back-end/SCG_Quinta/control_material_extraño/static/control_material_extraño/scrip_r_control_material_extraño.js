document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var turno = $("#turno").val();
            var areaMaterial = $("#area").val();
            var tipoMaterial = $("#tipo-material").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();
            var observaciones = $("#observaciones").val();

            // agregar valores a datos

            var datos = {
                turno: turno,
                area_material: areaMaterial,
                tipo_material: tipoMaterial,
                accion_correctiva: accionCorrectiva,
                verificacion_accion_correctiva: verificacionAccionCorrectiva,
                observaciones: observaciones
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/control_material_extraño/vista_control_material_extraño/', {
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
