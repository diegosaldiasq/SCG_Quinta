// Envio de datos a Django
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $("#descarga-monitoreo-del-agua").click(function() {
        var fechainicio = $("#fecha-inicio").val();
        var fechafin = $("#fecha-fin").val();
        

        $.ajax({
            url: "/inicio/descargar_monitoreo_del_agua/",  // Ruta a tu vista Django
            method: "POST",
            data: {
                fechainicio: fechainicio,
                fechafin: fechafin
            },
            success: function(response) {
                // Hacer algo con la respuesta del servidor
                //console.log(response);
                $("#mensaje").text(response.mensaje);
            },
            error: function() {
                // Manejar errores
                console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
            }
        });
    });
});