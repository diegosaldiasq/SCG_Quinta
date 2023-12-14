/*document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
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
});*/

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var fuenteMaterial = $("#fuente-material").val();
            var cantidadContaminada = $("#cantidad-cont").val();
            var unidadDeMedida = $("#udm").val();
            var loteProductoContaminado = $("#lote-prod-cont").val();
            var observaciones = $("#obs").val();
            var analisisCausa = $("#analisis-causa").val();
            var accionCorrectiva = $("#ac").val();

            // agregar valores a datos

            var datos = {
                fuente_material: fuenteMaterial,
                cantidad_contaminada: cantidadContaminada,
                unidad_de_medida: unidadDeMedida,
                lote_producto_contaminado: loteProductoContaminado,
                observaciones: observaciones,
                analisis_causa: analisisCausa,
                accion_correctiva: accionCorrectiva
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/informe_de_incidentes/vista_informe_de_incidentes/', {
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