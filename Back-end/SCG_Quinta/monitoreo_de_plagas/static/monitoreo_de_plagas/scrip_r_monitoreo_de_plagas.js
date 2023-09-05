const nombreTecnologo = document.querySelector('#nombre-tecnologo');
const fechaDeRegistro = document.querySelector('#fecha-reg');

const numeroDeEstacion = document.querySelector('#numero-estacion');
const tipoDePlaga = document.querySelector('#tipo-plaga');
const tipoDeTrampa = document.querySelector('#tipo-trampa');
const ubicacion = document.querySelector('#ubicacion');
const monitoreo = document.querySelector('#monitoreo');
const accionCorrectiva = document.querySelector('#ac');

$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/monitoreo_de_plagas/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                fecha_registro: fechaDeRegistro,
                numero_estacion: numeroDeEstacion,
                tipo_plaga: tipoDePlaga,
                tipo_trampa: tipoDeTrampa,
                ubicacion: ubicacion,
                monitoreo: monitoreo,
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