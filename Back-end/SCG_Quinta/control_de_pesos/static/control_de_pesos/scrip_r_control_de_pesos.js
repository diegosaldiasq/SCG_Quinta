document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var fechaRecepcion = $("#fecha-recep").val();
            var productoRecepcion = $("#producto").val();
            var temperaturaTransporte = $("#t-transporte").val();
            var temperaturaProducto = $("#t-producto").val();
            var lote = $("#lote").val();
            var fechaVencimiento = $("#fecha-venc").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();

            // agregar valores a datos

            var datos = {
                fecha_recepcion: fechaRecepcion,
                producto_recepcion: productoRecepcion,
                temperatura_transporte: temperaturaTransporte,
                temperatura_producto: temperaturaProducto,
                lote: lote,
                fecha_vencimiento: fechaVencimiento,
                accion_correctiva: accionCorrectiva,
                verificacion_accion_correctiva: verificacionAccionCorrectiva
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/control_de_pesos/vista_control_de_pesos/', {
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