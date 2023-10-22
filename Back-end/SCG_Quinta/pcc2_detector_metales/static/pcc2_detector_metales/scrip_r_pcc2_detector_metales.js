document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var fechaRegistro = document.getElementById('fecha-reg');
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
            var fechaRegistro = $("#fecha-reg").val();
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
                    fecha_registro: fechaRegistro,
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
});