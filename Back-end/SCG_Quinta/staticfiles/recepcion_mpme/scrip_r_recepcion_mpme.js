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