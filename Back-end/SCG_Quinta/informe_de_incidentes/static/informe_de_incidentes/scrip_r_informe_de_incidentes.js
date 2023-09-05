const nombreTecnologo = document.querySelector('#nomb-tecno');
const fechaRegistro = document.querySelector('#fecha-reg');

const fuenteMaterial = document.querySelector('#fuente-material');
const cantidadContaminada = document.querySelector('#cantidad-cont');
const unidadDeMedida = document.querySelector('#udm');
const loteProductoContaminado = document.querySelector('#lote-prod-cont');
const observaciones = document.querySelector('#obs');
const analisisCausa = document.querySelector('#analisis-causa');
const accionCorrectiva = document.querySelector('#ac');


$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "../../Back-end/SCG_Quinta/informe_de_incidentes/views.py",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                fecha_registro: fechaRegistro,
                fuente_material: fuenteMaterial,
                cantidad_contaminada: cantidadContaminada,
                unidad_de_medida: unidadDeMedida,
                lote_producto_contaminado: loteProductoContaminado,
                observaciones: observaciones,
                analisis_causa: analisisCausa,
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