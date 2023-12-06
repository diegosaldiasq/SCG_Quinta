/* document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var loteDia = document.getElementById('lote-dia');
    var nombreProveedor = document.getElementById('proveedor');
    var nombreProducto = document.getElementById('producto');
    var fechaDeElaboracion = document.getElementById('fecha-elab');
    var fechaDeVencimiento = document.getElementById('fecha-venc');
    var loteProducto = document.getElementById('lote-producto');
    var numeroFactura = document.getElementById('numero-factura')
    var higiene = document.getElementById('higiene');
    var rs = document.getElementById('rs');
    var temperaturaTransporte = document.getElementById('temperatura-trans');
    var apariencia = document.getElementById('apariencia');
    var textura = document.getElementById('textura');
    var ausenciaMaterialExtraño = document.getElementById('ausencia-me');
    var temperaturaProducto = document.getElementById('temperatura-prod');
    var condicionEnvase = document.getElementById('condicion-env');
    var color = document.getElementById('color');
    var olor = document.getElementById('olor');
    var sabor = document.getElementById('sabor');
    var gradosBrix = document.getElementById('grados-brix');

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
            var loteDia = $("#lote-dia").val();
            var nombreProveedor = $("#proveedor").val();
            var nombreProducto = $("#producto").val();
            var fechaDeElaboracion = $("#fecha-elab").val();
            var fechaDeVencimiento = $("#fecha-venc").val();
            var loteProducto = $("#lote-producto").val();
            var numeroFactura = $("#numero-factura").val();
            var higiene = $("#higiene").val();
            var rs = $("#rs").val();
            var temperaturaTransporte = $("#temperatura-trans").val();
            var apariencia = $("#apariencia").val();
            var textura = $("#textura").val();
            var ausenciaMaterialExtraño = $("#ausencia-me").val();
            var temperaturaProducto = $("#temperatura-prod").val();
            var condicionEnvase = $("#condicion-env").val();
            var color = $("#color").val();
            var olor = $("#olor").val();
            var sabor = $("#sabor").val();
            var gradosBrix = $("#grados-brix").val();
    
            $.ajax({
                url: "/recepcion_mpme/vista_recepcion_mpme/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    lote_dia: loteDia,
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
                    //Hacer algo con la respuesta del servidor
                    //console.log(response);
                    var mensaje;
                    if (response.mensaje === 'Datos guardados exitosamente') {
                        mensaje = response.mensaje;
                    } else {
                        mensaje = 'Error al guardar los datos';
                    }
                    alert(mensaje);
                },
                error: function() {
                    // Manejar errores
                    console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
                }
            });
        });
    });
}); */

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var loteDia = $("#lote-dia").val();
            var nombreProveedor = $("#proveedor").val();
            var nombreProducto = $("#producto").val();
            var fechaDeElaboracion = $("#fecha-elab").val();
            var fechaDeVencimiento = $("#fecha-venc").val();
            var loteProducto = $("#lote-producto").val();
            var numeroFactura = $("#numero-factura").val();
            var higiene = $("#higiene").val();
            var rs = $("#rs").val();
            var temperaturaTransporte = $("#temperatura-trans").val();
            var apariencia = $("#apariencia").val();
            var textura = $("#textura").val();
            var ausenciaMaterialExtraño = $("#ausencia-me").val();
            var temperaturaProducto = $("#temperatura-prod").val();
            var condicionEnvase = $("#condicion-env").val();
            var color = $("#color").val();
            var olor = $("#olor").val();
            var sabor = $("#sabor").val();
            var gradosBrix = $("#grados-brix").val();

            // agregar valores a datos

            var datos = {
                lote_dia: loteDia,
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
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/recepcion_mpme/vista_recepcion_mpme/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
                },
                body: JSON.stringify({ dato: datos })
            });
            var data = await response.json();
            debugger; // <-- Agrega esta línea
            if (data.existe) {
                alert("Datos guardados exitosamente!!");
                location.reload();
                return true;
            } else {
                alert("No se pudo guardar... revisa nuevamente!!");
                return false;
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al cargar los datos, formatos no coinciden!!");
        }
    });
});