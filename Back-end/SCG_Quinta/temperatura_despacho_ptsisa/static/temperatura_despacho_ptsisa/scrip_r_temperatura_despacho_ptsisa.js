document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var nombreTecnologo = document.getElementById('nombre-tecnologo');
    var fechaRegistro = document.getElementById('fecha-reg');

    var cadena = document.getElementById('cadena');
    var item = document.getElementById('item');
    var producto = document.getElementById('producto');
    var congeladoRefrigerado = document.getElementById('cong-refr');
    var temperaturaProducto = document.getElementById('t-producto');
    var revisionEtiquetado = document.getElementById('rev-etiquetado');
    var lote = document.getElementById('lote');
    var fechaVencimiento = document.getElementById('fecha-vencimiento');
    var accionCorrectiva = document.getElementById('ac');
    var verificacionAccionCorrectiva = document.getElementById('vac');

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
            $.ajax({
                url: "/temperatura_despacho_ptsisa/vista_temperatura_despacho_ptsisa/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    nombre_tecnologo: nombreTecnologo.value,
                    fecha_registro: fechaRegistro.value,
                    cadena: cadena.value,
                    item: item.value,
                    producto: producto.value,
                    congelado_refrigerado: congeladoRefrigerado.value,
                    temperatura_producto: temperaturaProducto.value,
                    revision_etiquetado: revisionEtiquetado.value,
                    lote: lote.value,
                    fecha_vencimiento: fechaVencimiento.value,
                    accion_correctiva: accionCorrectiva.value,
                    verificacion_accion_correctiva: verificacionAccionCorrectiva.value
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