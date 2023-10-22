document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var fechaRegistro = document.getElementById('fecha-reg');

    var turno = document.getElementById('turno');
    var planta = document.getElementById('planta');
    var numeroLlave = document.getElementById('numero-llave');
    var puntoMuestreo = document.getElementById('punto-muestreo');
    var saborInsipido = document.getElementById('sabor-insipido');
    var olorInodora = document.getElementById('olor-inodora');
    var colorIcoloro = document.getElementById('color-incoloro');
    var ph = document.getElementById('ph');
    var cloroLibre = document.getElementById('cloro-libre');
    var accionCorrectiva = document.getElementById('ac');
    var resultadoAc = document.getElementById('resultado-ac');

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
            var planta = $("#planta").val();
            var numeroLlave = $("#numero-llave").val();
            var puntoMuestreo = $("#punto-muestreo").val();
            var saborInsipido = $("#sabor-insipido").val();
            var olorInodora = $("#olor-inodora").val();
            var colorIcoloro = $("#color-incoloro").val();
            var ph = $("#ph").val();
            var cloroLibre = $("#cloro-libre").val();
            var accionCorrectiva = $("#ac").val();
            var resultadoAc = $("#resultado-ac").val();
    
            $.ajax({
                url: "/monitoreo_del_agua/vista_monitoreo_del_agua/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    fecha_registro: fechaRegistro,
                    turno_mda: turno,
                    planta_mda: planta,
                    numero_llave: numeroLlave,
                    punto_muestreo: puntoMuestreo,
                    sabor_insipido: saborInsipido,
                    olor_inodora: olorInodora,
                    color_incoloro: colorIcoloro,
                    ph_mda: ph,
                    cloro_libre: cloroLibre,
                    accion_correctiva: accionCorrectiva,
                    resultado_ac: resultadoAc
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







