const nombreTecnologo = document.querySelector('#nombre-tecnologo');
const fechaRegistro = document.querySelector('#fecha-reg');

const turno = document.querySelector('#turno');
const planta = document.querySelector('#planta');
const numeroLlave = document.querySelector('#numero-llave');
const puntoMuestreo = document.querySelector('#punto-muestreo');
const saborInsipido = document.querySelector('#sabor-insipido');
const olorInodora = document.querySelector('#olor-inodora');
const colorIcoloro = document.querySelector('#color-incoloro');
const ph = document.querySelector('#ph');
const cloroLibre = document.querySelector('#cloro-libre');
const accionCorrectiva = document.querySelector('#ac');
const resultadoAc = document.querySelector('#resultado-ac');

$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/monitoreo_del_agua/views.py",  // Ruta a tu vista Django
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
            },
            error: function() {
                // Manejar errores
            }
        });
    });
});