document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí

    // Envio de datos a Django
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }       
        }
    });

    $(document).ready(function() {
        $("#miBoton").click(function() {
            var cadena = $("#cadena").val();
            var item = $("#item").val();
            var producto = $("#producto").val();
            var temperaturaProducto = $("#t-producto").val();
            var revisionEtiquetado = $("#rev-etiquetado").val();
            var lote = $("#lote").val();
            var fechaVencimiento = $("#fecha-vencimiento").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();

            $.ajax({
                url: "/temperatura_despacho_ptjumbo/vista_temperatura_despacho_ptjumbo/",  // Ruta a tu vista Django
                method: "POST",
                data: {
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
                    $("#mensaje").text(response.mensaje);
                },
                error: function() {
                    // Manejar errores
                    console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
                }
            });
        });
    });
});