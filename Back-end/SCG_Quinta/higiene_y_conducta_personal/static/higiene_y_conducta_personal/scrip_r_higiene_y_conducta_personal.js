document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var fechaIngreso = document.getElementById('fecha-ingreso');
    var nombrePersonal = document.getElementById('nombre-personal');
    var turno = document.getElementById('turno');
    var planta = document.getElementById('planta');
    var area = document.getElementById('area');
    var cumplimiento = document.getElementById('cumpl');
    var desviacion = document.getElementById('desv');
    var accionCorrectiva = document.getElementById('ac');
    var verificacionAccionCorrectiva = document.getElementById('vac');
    var observacion = document.getElementById('obs');
    var nombreTecnologo = document.getElementById('nomb-tecno');

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
            var fechaIngreso = $("#fecha-ingreso").val();
            var nombrePersonal = $("#nombre-personal").val();
            var turno = $("#turno").val();
            var planta = $("#planta").val();
            var area = $("#area").val();
            var cumplimiento = $("#cumpl").val();
            var desviacion = $("#desv").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();
            var observacion = $("#obs").val();
            var nombreTecnologo = $("#nomb-tecno").val();

            $.ajax({
                url: "/higiene_y_conducta_personal/vista_higiene_y_conducta_personal/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    fecha_ingreso: fechaIngreso,
                    nombre_personal: nombrePersonal,
                    turno: turno,
                    planta: planta,
                    area: area,
                    cumplimiento: cumplimiento,
                    desviacion: desviacion,
                    accion_correctiva: accionCorrectiva,
                    verificacion_accion_correctiva: verificacionAccionCorrectiva,
                    observacion: observacion,
                    nombre_tecnologo: nombreTecnologo
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
    alert("El archivo JavaScript se ha cargado y la página está lista.");
});
