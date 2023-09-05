const nombreTecnologo = document.querySelector('#nombre-tecnologo');
const fechaRegistro = document.querySelector('#fecha-reg');

const cadena = document.querySelector('#cadena');
const item = document.querySelector('#item');
const producto = document.querySelector('#producto');
const temperaturaProducto = document.querySelector('#t-producto');
const revisionEtiquetado = document.querySelector('#rev-etiquetado');
const lote = document.querySelector('#lote');
const fechaVencimiento = document.querySelector('#fecha-vencimiento');
const accionCorrectiva = document.querySelector('#ac');
const verificacionAccionCorrectiva = document.querySelector('#vac');


$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/temperatura_despacho_ptjumbo/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                fecha_registro: fechaRegistro,
                cadena: cadena,
                item: item,
                producto: producto,
                temperatura_producto: temperaturaProducto,
                revision_etiquetado: revisionEtiquetado,
                lote: lote,
                fecha_vencimiento: fechaVencimiento,
                accion_correctiva: accionCorrectiva,
                verificacion_accion_correctiva: verificacionAccionCorrectiva
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