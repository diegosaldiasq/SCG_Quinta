// static/login/scrips_main.js

// Configuración global de jQuery para incluir CSRF en todas las peticiones POST/AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Capturamos el evento 'submit' del formulario en lugar de 'click' en un botón
    document.getElementById("miBoton").addEventListener("submit", async function(event) {
        event.preventDefault(); // <-- Evita que el formulario recargue la página

        try {
            // Obtenemos los valores ingresados en los campos
            var nombreCompleto = $("#nombre-completo").val();
            var perfilUsuario = $("#perfil-usuario").val();
            var rut = $("#rut").val();
            var password = $("#password").val();

            // Creamos el objeto JSON con las mismas claves que leerá la vista Django
            var datos = {
                nombreCompleto:nombreCompleto,
                perfilUsuario:perfilUsuario,
                rut:rut,
                pasword:password
            };

            // Enviamos la petición fetch al endpoint /login/vista_main/
            var response = await fetch("/login/vista_main/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(datos)
            });

            // Si la respuesta NO es HTTP 2xx, mostramos alerta y detenemos
            if (!response.ok) {
                console.warn("Respuesta no OK del servidor:", response.status);
                alert("Error en la petición: código " + response.status);
                return;
            }

            // Parseamos el cuerpo como JSON (ahora sí es JSON si response.ok)
            var data = await response.json();

            // Depuración (opcional)
            console.log("Respuesta JSON de vista_main:", data);

            if (data.existe) {
                //alert("Ingreso correcto!!!");
                // Aquí puedes redirigir a otra URL si lo deseas
                window.location.href = "/inicio/index/";
            } else {
                alert("No se pudo entrar... revisa nuevamente!!");
            }

        } catch (error) {
            console.error("Hubo un error en el fetch:", error);
            alert("Hubo un problema al verificar los datos.");
        }
    });
});
