const nombreTecnologo = document.querySelector('#nombre-tecnologo');
const loteDia = document.querySelector('#lote-dia');
const fechaRegistro = document.querySelector('#fecha-reg');

const nombreProveedor = document.querySelector('#proveedor');
const nombreProducto = document.querySelector('#producto');
const fechaDeElaboracion = document.querySelector('#fecha-elab');
const fechaDeVencimiento = document.querySelector('#fecha-venc');
const loteProducto = document.querySelector('#lote-producto');
const numeroFactura = document.querySelector('#numero-factura')
const higiene = document.querySelector('#higiene');
const rs = document.querySelector('#rs');
const temperaturaTransporte = document.querySelector('#temperatura-trans');
const apariencia = document.querySelector('#apariencia');
const textura = document.querySelector('#textura');
const ausenciaMaterialExtraño = document.querySelector('#ausencia-me');
const temperaturaProducto = document.querySelector('#temperatura-prod');
const condicionEnvase = document.querySelector('#condicion-env');
const color = document.querySelector('#color');
const olor = document.querySelector('#olor');
const sabor = document.querySelector('#sabor');
const gradosBrix = document.querySelector('#grados-brix');


$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/recepcion_mpme/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                lote_dia: loteDia,
                fecha_registro: fechaRegistro,
                nombre_proveedor: nombreProveedor,
                nombre_producto: nombreProducto,
                fecha_elaboracion: fechaDeElaboracion,
                fecha_vencimiento: fechaDeVencimiento,
                lote_producto: loteProducto,
                numero_factura: numeroFactura,
                higiene: higiene,
                rs: rs,
                temperatura_transporte: temperaturaTransporte,
                apariencia: apariencia,
                textura: textura,
                ausencia_material_extraño: ausenciaMaterialExtraño,
                temperatura_producto: temperaturaProducto,
                condicion_envase: condicionEnvase,
                color: color,
                olor: olor,
                sabor: sabor,
                grados_brix: gradosBrix
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