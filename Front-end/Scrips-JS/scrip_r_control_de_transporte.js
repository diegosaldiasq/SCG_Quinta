const nombreTecnologo = document.querySelector('#nom-tec');
const fechaRegistro = document.querySelector('#fecha-reg');

const fechaRecepcion = document.querySelector('#fecha-recep');
const productoRecepcion = document.querySelector('#producto');
const temperaturaTransporte = document.querySelector('#t-transporte');
const temperaturaProducto = document.querySelector('#t-producto');
const lote = document.querySelector('#lote');
const fechaVencimiento = document.querySelector('#fecha-venc');
const accionCorrectiva = document.querySelector('#ac');
const verificacionAccionCorrectiva = document.querySelector('#vac');


$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/control_de_transporte/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                fecha_registro: fechaRegistro,
                fecha_recepcion: fechaRecepcion,
                producto_recepcion: productoRecepcion,
                temperatura_transporte: temperaturaTransporte,
                temperatura_producto: temperaturaProducto,
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