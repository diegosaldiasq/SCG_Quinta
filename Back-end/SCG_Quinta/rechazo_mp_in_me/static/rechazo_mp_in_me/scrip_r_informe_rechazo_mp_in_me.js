const nombreTecnologo = document.querySelector('#nomb-tecn');
const fechaRegistro = document.querySelector('#fecha-reg');

const nombreDeProveedor = document.querySelector('#nomb-prov');
const numeroFactura = document.querySelector('#numero-factura');
const nombreDelTransportista = document.querySelector('#nomb-trans');

const nombreProducto = document.querySelector('#nombre-producto');
const fechaElaboracion = document.querySelector('#fecha-elab');
const lote = document.querySelector('#lote');
const fechaVencimiento = document.querySelector('#fecha-venc');
const motivoRechazo = document.querySelector('#motivo-rechazo');
const cantidadProductoInvolucrado = document.querySelector('#cantidad-producto');
const unidadDeMedida = document.querySelector('#udm');
const clasificacion = document.querySelector('#clasificacion');

$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/temperatura_despacho_ptjumbo/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                fecha_registro: fechaRegistro,
                nombre_proveedor: nombreDeProveedor,
                numero_factura: numeroFactura,
                nombre_transportista: nombreDelTransportista,
                nombre_producto: nombreProducto,
                fecha_elaboracion: fechaElaboracion,
                lote: lote,
                fecha_vencimiento: fechaVencimiento,
                motivo_rechazo: motivoRechazo,
                cantidad_producto_involucrado: cantidadProductoInvolucrado,
                unidad_de_medida: unidadDeMedida,
                clasificacion: clasificacion
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