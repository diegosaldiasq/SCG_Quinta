document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var nombreTecnologo = document.getElementById('nomb-tecno');
    var fechaRegistro = document.getElementById('fecha-reg');

    var fuenteMaterial = document.getElementById('fuente-material');
    var cantidadContaminada = document.getElementById('cantidad-cont');
    var unidadDeMedida = document.getElementById('udm');
    var loteProductoContaminado = document.getElementById('lote-prod-cont');
    var observaciones = document.getAnimations('obs');
    var analisisCausa = document.getElementById('analisis-causa');
    var accionCorrectiva = document.getElementById('ac');

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

            var nombreTecnologo = $("#nomb-tecno").val();
            var fechaRegistro = $("#fecha-reg").val();
            var fuenteMaterial = $("#fuente-material").val();
            var cantidadContaminada = $("#cantidad-cont").val();
            var unidadDeMedida = $("#udm").val();
            var loteProductoContaminado = $("#lote-prod-cont").val();
            var observaciones = $("#obs").val();
            var analisisCausa = $("#analisis-causa").val();
            var accionCorrectiva = $("#ac").val();

            $.ajax({
                url: "/informe_de_incidentes/vista_informe_de_incidentes/",  // Ruta a tu vista Django
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
                    $("#mensaje").text(response.mensaje);
                },
                error: function() {
                    // Manejar errores
                    console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
                }
            });
        });
    });   
    alert("El archivo JavaScript se ha cargado y la página está lista.");
});