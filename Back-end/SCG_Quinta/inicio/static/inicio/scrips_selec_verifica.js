document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("monitoreo-del-agua").addEventListener("click", async function() {
        try {
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            userData = "monitoreo-del-agua"

            var response = await fetch('/inicio/verificar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
                },
                body: JSON.stringify({ "userData": userData })
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