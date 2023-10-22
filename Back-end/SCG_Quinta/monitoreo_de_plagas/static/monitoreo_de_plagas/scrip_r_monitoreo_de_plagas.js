document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var fechaDeRegistro = document.getElementById('fecha-reg');

    var numeroDeEstacion = document.getElementById('numero-estacion');
    var tipoDePlaga = document.getElementById('tipo-plaga');
    var tipoDeTrampa = document.getElementById('tipo-trampa');
    var ubicacion = document.getElementById('ubicacion');
    var monitoreo = document.getElementById('monitoreo');
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
            var fechaDeRegistro = $("#fecha-reg").val();
            var numeroDeEstacion = $("#numero-estacion").val();
            var tipoDePlaga = $("#tipo-plaga").val();
            var tipoDeTrampa = $("#tipo-trampa").val();
            var ubicacion = $("#ubicacion").val();
            var monitoreo = $("#monitoreo").val();
            var accionCorrectiva = $("#ac").val();
    
            $.ajax({
                url: "/monitoreo_de_plagas/vista_monitoreo_de_plagas/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    fecha_registro: fechaDeRegistro,
                    numero_estacion: numeroDeEstacion,
                    tipo_plaga: tipoDePlaga,
                    tipo_trampa: tipoDeTrampa,
                    ubicacion: ubicacion,
                    monitoreo: monitoreo,
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
    alert("El archivo JavaScript se ha cargado y la página está lista.");
});