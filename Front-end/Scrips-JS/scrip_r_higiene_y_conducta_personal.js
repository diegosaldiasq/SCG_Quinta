const fechaIngreso = document.querySelector('#fecha-ingreso');
const nombrePersonal = document.querySelector('#nombre-personal');
const turno = document.querySelector('#turno');
const planta = document.querySelector('#planta');
const area = document.querySelector('#area');
const cumplimiento = document.querySelector('#cumpl');
const desviacion = document.querySelector('#desv');
const accionCorrectiva = document.querySelector('#ac');
const verificacionAccionCorrectiva = document.querySelector('#vac');
const observacion = document.querySelector('#obs');
const nombreTecnologo = document.querySelector('#nomb-tecno');


$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/higiene_y_conducta_personal/views.py",  // Ruta a tu vista Django
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
            },
            error: function() {
                // Manejar errores
            }
        });
    });
});