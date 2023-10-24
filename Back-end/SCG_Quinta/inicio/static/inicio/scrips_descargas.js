document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var userData = [];

            let users = document.querySelectorAll('.usuario');

            users.forEach(function(user) {
                let name = user.querySelector('span').innerText;
                let isActive = user.querySelectorAll('input[type="checkbox"]')[0].checked;
                let isStaff = user.querySelectorAll('input[type="checkbox"]')[1].checked;
        
                userData.push({
                    name: name,
                    isActive: isActive,
                    isStaff: isStaff
                });
            });          
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/inicio/vista_permisos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
                },
                body: JSON.stringify({ userData: userData })
            });
            var data = await response.json();
            debugger; // <-- Agrega esta línea
            if (data.existe) {
                //window.location.href = "/inicio/permiso_creado/";
                alert("Se actualizaron los permisos correctamente.");
                return true;
            } else {
                alert("No se pudo actualizar los permisos.");
                return false;
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al guardar los permisos.");
        }
    });
});