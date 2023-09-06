const nombreTecnologo = document.querySelector('#nomb-tec');
const fechaRegistro = document.querySelector('#fecha-reg');
const turno = document.querySelector('#turno');

const areaMaterial = document.querySelector('#area');
const tipoMaterial = document.querySelector('#tipo-material');
const accionCorrectiva = document.querySelector('#ac');
const verificacionAccionCorrectiva = document.querySelector('#vac');
const observaciones = document.querySelector('#observaciones');


$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "/control_material_extraño/",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
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
            },
            error: function() {
                // Manejar errores
            }
        });
    });
});
