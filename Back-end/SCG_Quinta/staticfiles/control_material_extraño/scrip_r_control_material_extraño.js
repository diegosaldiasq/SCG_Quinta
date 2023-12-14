/*document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var turno = document.getElementById('turno');

    var areaMaterial = document.getElementById('area');
    var tipoMaterial = document.getElementById('tipo-material');
    var accionCorrectiva = document.getElementById('ac');
    var verificacionAccionCorrectiva = document.getElementById('vac');
    var observaciones = document.getElementById('observaciones');

    // Envio de datos a Django
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).ready(function() {
        $("#miBoton").click(function() {
            var turno = $("#turno").val();
            var areaMaterial = $("#area").val();
            var tipoMaterial = $("#tipo-material").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();
            var observaciones = $("#observaciones").val();

            $.ajax({
                url: "/control_material_extraño/vista_control_material_extraño/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    turno: turno,
                    area_material: areaMaterial,
                    tipo_material: tipoMaterial,
                    accion_correctiva: accionCorrectiva,
                    verificacion_accion_correctiva: verificacionAccionCorrectiva,
                    observaciones: observaciones
                },
                success: function(response) {
                    // Hacer algo con la respuesta del servidor
                    console.log(response);
                    $("#mensaje").text(response.mensaje);
                },
                error: function() {
                    // Manejar errores
                    console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
                }
            });
        });
    });
});*/

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
