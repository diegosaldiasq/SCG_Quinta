document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
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

            // agregar valores a datos

            var datos = {
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
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/rechazo_mp_in_me/vista_rechazo_mp_in_me/', {
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