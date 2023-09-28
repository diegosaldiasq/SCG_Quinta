document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var nombreTecnologo = document.getElementById('nomb-tecn');
    var fechaRegistro = document.getElementById('fecha-reg');

    var nombreDeProveedor = document.getElementById('nomb-prov');
    var numeroFactura = document.getElementById('numero-factura');
    var nombreDelTransportista = document.getElementById('nomb-trans');

    var nombreProducto = document.getElementById('nombre-producto');
    var fechaElaboracion = document.getElementById('fecha-elab');
    var lote = document.getElementById('lote');
    var fechaVencimiento = document.getElementById('fecha-venc');
    var motivoRechazo = document.getElementById('motivo-rechazo');
    var cantidadProductoInvolucrado = document.getElementById('cantidad-producto');
    var unidadDeMedida = document.getElementById('udm');
    var clasificacion = document.getElementById('clasificacion');

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

            var nombreTecnologo = $("#nomb-tecn").val();
            var fechaRegistro = $("#fecha-reg").val();
            var nombreDeProveedor = $("#nomb-prov").val();
            var numeroFactura = $("#numero-factura").val();
            var nombreDelTransportista = $("#nomb-trans").val();
            var nombreProducto = $("#nombre-producto").val();
            var fechaElaboracion = $("#fecha-elab").val();
            var lote = $("#lote").val();
            var fechaVencimiento = $("#fecha-venc").val();
            var motivoRechazo = $("#motivo-rechazo").val();
            var cantidadProductoInvolucrado = $("#cantidad-producto").val();
            var unidadDeMedida = $("#udm").val();
            var clasificacion = $("#clasificacion").val();

            $.ajax({
                url: "/rechazo_mp_in_me/vista_rechazo_mp_in_me/",  // Ruta a tu vista Django
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