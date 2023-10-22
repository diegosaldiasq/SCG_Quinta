document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var fechaRegistro = document.getElementById('fecha-reg');

    var nombreProveedor = document.getElementById('nombre-prov');
    var fechaReclamo = document.getElementById('fecha-recl');

    var nombreDelProducto = document.getElementById('nombre-prod');
    var fechaDeElaboracion = document.getElementById('fecha-elab');
    var lote = document.getElementById('lote');
    var fechaDeVencimiento = document.getElementById('fecha-venc');
    var noConformidad = document.getElementById('no-conf');

    var clasificacion = document.querySelector('clasificacion');
    var cantidadInvolucrada = document.querySelector('cantidad-inv');
    var unidadDeMedida = document.querySelector('udm')
    var archivoFoto = document.querySelector('archivo-foto');

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
            var fechaRegistro = $("#fecha-reg").val();
            var nombreProveedor = $("#nombre-prov").val();
            var fechaReclamo = $("#fecha-recl").val();
            var nombreDelProducto = $("#nombre-prod").val();
            var fechaDeElaboracion = $("#fecha-elab").val();
            var lote = $("#lote").val();
            var fechaDeVencimiento = $("#fecha-venc").val();
            var noConformidad = $("#no-conf").val();
            var clasificacion = $("#clasificacion").val();
            var cantidadInvolucrada = $("#cantidad-inv").val();
            var unidadDeMedida = $("#udm").val();
            var archivoFoto = $("#archivo-foto").val();

            $.ajax({
                url: "/reclamo_a_proveedores/vista_reclamo_a_proveedores/",  // Ruta a tu vista Django
                method: "POST",
                data: {
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
                    $("#mensaje").text(response.mensaje);
                },
            });
        });
    });
    // Fin de envio de datos a Django
});