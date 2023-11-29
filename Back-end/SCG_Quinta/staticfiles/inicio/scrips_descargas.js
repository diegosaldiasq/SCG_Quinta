// Envio de datos a Django
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $("#filtrar-fechas").click(function() {
        event.preventDefault();
        var fechainicio = $("#fecha-inicio").val();
        var fechafin = $("#fecha-fin").val();
        

        $.ajax({
            url: "/inicio/set_fechas/",  // Ruta a tu vista Django
            method: "POST",
            data: {
                'fechainicio': fechainicio,
                'fechafin': fechafin
            },
            success: function(response) {
                if (response.success) {
                    alert("Fechas establecidas. Ahora puedes descargar los informes.");
                }
                else {
                    alert("Error al establecer fechas");
                }
            },
            error: function() {
                console.error("Error al establecer fechas");
                alert("Error al establecer fechas");
            }
        });
    });
});