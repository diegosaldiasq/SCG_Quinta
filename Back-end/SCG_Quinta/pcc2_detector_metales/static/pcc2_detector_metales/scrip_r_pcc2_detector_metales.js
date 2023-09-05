const nombreTecnologo = document.querySelector('#nombre-tecnologo');
const fechaRegistro = document.querySelector('#fecha-reg');
const lote = document.querySelector('#lote');
const turno = document.querySelector('#turno');

const tipoMetal = document.querySelector('#tipo-metal');
const medicion = document.querySelector('#medicion');
const producto =  document.querySelector('#producto');
const observaciones = document.querySelector('#obs');
const accionCorrectiva = document.querySelector('#ac')

$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/pcc2_detector_metales/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
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
            },
            error: function() {
                // Manejar errores
            }
        });
    });
});