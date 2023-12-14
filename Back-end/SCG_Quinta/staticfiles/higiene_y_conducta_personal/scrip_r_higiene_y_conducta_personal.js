/*document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var nombrePersonal = document.getElementById('nombre-personal');
    var turno = document.getElementById('turno');
    var planta = document.getElementById('planta');
    var area = document.getElementById('area');
    var cumplimiento = document.getElementById('cumpl');
    var desviacion = document.getElementById('desv');
    var accionCorrectiva = document.getElementById('ac');
    var verificacionAccionCorrectiva = document.getElementById('vac');
    var observacion = document.getElementById('obs');
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
            var nombrePersonal = $("#nombre-personal").val();
            var turno = $("#turno").val();
            var planta = $("#planta").val();
            var area = $("#area").val();
            var cumplimiento = $("#cumpl").val();
            var desviacion = $("#desv").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();
            var observacion = $("#obs").val();

            $.ajax({
                url: "/higiene_y_conducta_personal/vista_higiene_y_conducta_personal/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    nombre_personal: nombrePersonal,
                    turno: turno,
                    planta: planta,
                    area: area,
                    cumplimiento: cumplimiento,
                    desviacion: desviacion,
                    accion_correctiva: accionCorrectiva,
                    verificacion_accion_correctiva: verificacionAccionCorrectiva,
                    observacion: observacion
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
