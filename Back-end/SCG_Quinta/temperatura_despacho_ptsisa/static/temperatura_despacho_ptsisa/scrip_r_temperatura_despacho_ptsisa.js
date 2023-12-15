/*document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
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
});*/

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
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

            // agregar valores a datos

            var datos = {
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
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/temperatura_despacho_ptsisa/vista_temperatura_despacho_ptsisa/', {
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