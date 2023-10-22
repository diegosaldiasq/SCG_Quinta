document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var fechaRegistro = document.getElementById('fecha-reg');
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
            var fechaRegistro = $("#fecha-reg").val();
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
                    fecha_registro: fechaRegistro,
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
    alert("El archivo JavaScript se ha cargado y la página está lista.");
});
