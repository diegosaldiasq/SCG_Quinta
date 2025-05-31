$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      // Si no es una petición GET/HEAD/OPTIONS o TRACE, agregamos el header
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var nombreCompleto = document.getElementById("nombre-completo").value;
            var perfilUsuario = document.getElementById("perfil-usuario").value;
            var rut = document.getElementById("rut").value;
            var pasword = document.getElementById("password").value;
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/login/vista_main/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
                },
                body: JSON.stringify({
                    nombreCompleto,
                    perfilUsuario,
                    rut,
                    pasword
                 })
            });
            var responseData = await response.json();

            if (responseData.existe) {
                window.location.href = "/inicio/index/";
            } else {
                alert("No se pudo ingresar a la cuenta: datos incorrectos.");
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al verificar el usuario.");
        }
    });
});