// Envio de datos a Django
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var pasword = document.getElementById("password").value;
            var newPasword = document.getElementById("new-password").value;

            if (pasword != newPasword) {
                alert("Las contraseñas no coinciden");
                return false;
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/login/vista_pasword/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
                },
                body: JSON.stringify({ dato: pasword })
            });
            var data = await response.json();
            debugger; // <-- Agrega esta línea
            if (data.existe) {
                window.location.href = "/login/pasword_creado/";
                //alert("El rut existe en la base de datos.");
                return true;
            } else {
                alert("No se pudo actualizar la contraseña.");
                return false;
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al verificar el usuario.");
        }
    });
});