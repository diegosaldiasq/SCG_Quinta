/*document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var fechaRecepcion = document.getElementById('fecha-recep');
    var productoRecepcion = document.getElementById('producto');
    var temperaturaTransporte = document.getElementById('t-transporte');
    var temperaturaProducto = document.getElementById('t-producto');
    var lote = document.getElementById('lote');
    var fechaVencimiento = document.getElementById('fecha-venc');
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
            var fechaRecepcion = $("#fecha-recep").val();
            var productoRecepcion = $("#producto").val();
            var temperaturaTransporte = $("#t-transporte").val();
            var temperaturaProducto = $("#t-producto").val();
            var lote = $("#lote").val();
            var fechaVencimiento = $("#fecha-venc").val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();
    
            $.ajax({
                url: "/control_de_transporte/vista_control_de_transporte/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    fecha_recepcion: fechaRecepcion,
                    producto_recepcion: productoRecepcion,
                    temperatura_transporte: temperaturaTransporte,
                    temperatura_producto: temperaturaProducto,
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
});*/

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

            var response = await fetch('/control_de_transporte/vista_control_de_transporte/', {
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