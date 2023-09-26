var nombreTecnologo = document.querySelector('#nombre-tecnologo');
var fechaRegistro = document.querySelector('#fecha-reg');

var turno = document.querySelector('#turno');
var planta = document.querySelector('#planta');
var numeroLlave = document.querySelector('#numero-llave');
var puntoMuestreo = document.querySelector('#punto-muestreo');
var saborInsipido = document.querySelector('#sabor-insipido');
var olorInodora = document.querySelector('#olor-inodora');
var colorIcoloro = document.querySelector('#color-incoloro');
var ph = document.querySelector('#ph');
var cloroLibre = document.querySelector('#cloro-libre');
var accionCorrectiva = document.querySelector('#ac');
var resultadoAc = document.querySelector('#resultado-ac');

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
        var nombreTecnologo = $("#nombre-tecnologo").val();
        var fechaRegistro = $("#fecha-reg").val();
        var turno = $("#turno").val();
        var planta = $("#planta");
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
                nombre_tecnologo: nombreTecnologo,
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