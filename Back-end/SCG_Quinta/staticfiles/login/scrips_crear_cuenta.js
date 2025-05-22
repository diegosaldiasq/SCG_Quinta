//document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
//    var nombreCompleto = document.getElementById('nombre-completo');
//    var perfilUsuario = document.getElementById('perfil-usuario');
//    var rut = document.getElementById('rut');
//    var password = document.getElementById('password');
//    var newPassword = document.getElementById('new-password');

    // Envio de datos a Django
//    $.ajaxSetup({
//        beforeSend: function(xhr, settings) {
//            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
//                xhr.setRequestHeader("X-CSRFToken", csrftoken);
//            }
//        }
//    });

//    $(document).ready(function() {
//        $("#miBoton").click(function() {
//            var nombreCompleto = $("#nombre-completo").val();
//            var perfilUsuario = $("#perfil-usuario").val();
//            var rut = $("#rut").val();
//            var password = $("#password").val();
//            var newPassword = $("#new-password").val();

//            if (password != newPassword) {  // Si las contraseñas no coinciden  
//                alert("Las contraseñas no coinciden");
//                return false;
//            }
    
//            $.ajax({
//                url: "/login/vista_crear_cuenta/",  // Ruta a tu vista Django
//                method: "POST",
//                data: {
//                    nombre_completo: nombreCompleto,
//                    perfil_usuario: perfilUsuario,
//                    rut: rut,
//                    password: password,
//                    new_password: newPassword
//                },
//                success: function(response) {
//                    // Hacer algo con la respuesta del servidor
//                    console.log(response);
//                    // Aquí puedes manejar la respuesta del servidor
//                    window.location.href = "/login/cuenta_creada/";
//                    $("#mensaje").text(response.mensaje);
//                },
//                error: function(response) {
//                    // Manejar errores
//                    console.error("Error en la solicitud AJAX:", response);
//                    alert("Error al crear la cuenta. Por favor, inténtalo de nuevo.");
//                },
//                error: function() {
//                    // Manejar errores
//                    console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
//                }
//            });
//        }); 
//    });
//});


document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var nombreCompleto = document.getElementById('nombre-completo');
    var perfilUsuario = document.getElementById('perfil-usuario');
    var rut = document.getElementById('rut');
    var password = document.getElementById('password');
    var newPassword = document.getElementById('new-password');

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
            var nombreCompleto = $("#nombre-completo").val();
            var perfilUsuario = $("#perfil-usuario").val();
            var rut = $("#rut").val();
            var password = $("#password").val();
            var newPassword = $("#new-password").val();

            if (password != newPassword) {  // Si las contraseñas no coinciden  
                alert("Las contraseñas no coinciden");
                return false;
            }
    
            $.ajax({
                url: "/login/vista_crear_cuenta/",  // Ruta a tu vista Django
                method: "POST",
                data: {
                    nombre_completo: nombreCompleto,
                    perfil_usuario: perfilUsuario,
                    rut: rut,
                    password: password,
                    new_password: newPassword
                },
                success: function(response) {
                    // Hacer algo con la respuesta del servidor
                    console.log(response);
                    $("#mensaje").text(response.mensaje);
                    window.location.href = "/login/cuenta_creada/";
                },
                error: function(response) {
                    // Manejar errores
                    console.error("Error en la solicitud AJAX:", response);
                    alert("Error al crear la cuenta. Por favor, inténtalo de nuevo.");
                },
                error: function() {
                    // Manejar errores
                    console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
                }
            });
        }); 
    });
});