/*document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var lote = document.getElementById('lote');
    var turno = document.getElementById('turno');

    var tipoMetal = document.getElementById('tipo-metal');
    var medicion = document.getElementById('medicion');
    var producto =  document.getElementById('producto');
    var observaciones = document.getElementById('obs');
    var accionCorrectiva = document.getElementById('ac');

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
            var lote = $("#lote").val();
            var turno = $("#turno").val();
            var tipoMetal = $("#tipo-metal").val();
            var medicion = $("#medicion").val();
            var producto =  $("#producto").val();
            var observaciones = $("#obs").val();
            var accionCorrectiva = $("#ac").val();
    
            $.ajax({
                url: "/pcc2_detector_metales/vista_pcc2_detector_metales/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    lote: lote,
                    turno: turno,
                    tipo_metal: tipoMetal,
                    medicion: medicion,
                    producto: producto,
                    observaciones: observaciones,
                    accion_correctiva: accionCorrectiva
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