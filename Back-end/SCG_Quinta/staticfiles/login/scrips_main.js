document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var nombreCompleto = $("#nombre-completo").val();
            var perfilUsuario = $("#perfil-usuario").val();
            var rut = $("#rut").val();
            var password = $("#pasword").val();

            // agregar valores a datos

            var datos = {
                nombreCompleto: nombreCompleto,
                perfilUsuario: perfilUsuario,
                rut: rut,
                password: password
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/login/vista_main/', {
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
                alert("Ingreso correcto!!!");
                location.reload();
            } else {
                alert("No se pudo entrar... revisa nuevamente!!");
                return false;
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al cargar los datos, formatos no coinciden!!");
        }
    });
});