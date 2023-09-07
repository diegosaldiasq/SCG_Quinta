const nombreTecnologo = document.querySelector('#nombre-tecnologo');
const fechaRegistro = document.querySelector('#fecha-reg');

const nombreProveedor = document.querySelector('#nombre-prov');
const fechaReclamo = document.querySelector('#fecha-recl');

const nombreDelProducto = document.querySelector('#nombre-prod');
const fechaDeElaboracion = document.querySelector('#fecha-elab');
const lote = document.querySelector('#lote');
const fechaDeVencimiento = document.querySelector('#fecha-venc');
const noConformidad = document.querySelector('#no-conf');

const clasificacion = document.querySelector('#clasificacion');
const cantidadInvolucrada = document.querySelector('#cantidad-inv');
const unidadDeMedida = document.querySelector('#udm')
const archivoFoto = document.querySelector('#archivo-foto');

$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/temperatura_despacho_ptjumbo/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                fecha_registro: fechaRegistro,
                nombre_proveedor: nombreProveedor,
                fecha_reclamo: fechaReclamo,
                nombre_del_producto: nombreDelProducto,
                fecha_elaboracion: fechaDeElaboracion,
                lote: lote,
                fecha_vencimiento: fechaDeVencimiento,
                no_conformidad: noConformidad,
                clasificacion: clasificacion,
                cantidad_involucrada: cantidadInvolucrada,
                unidad_de_medida: unidadDeMedida,
                archivo_foto: archivoFoto
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