document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton_monitoreo_del_agua").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var userData = [];

            let datos = document.querySelectorAll('.usuario_monitoreo_del_agua');

            datos.forEach(function(dato) {
                let id = dato.querySelectorAll('.id').innerText;
                let isVerificado = dato.querySelectorAll('.checkbox_monitoreo_del_agua').checked;
        
                userData.push({
                    id: id,
                    isVerificado: isVerificado
                });
            });          
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/inicio/verificar_monitoreo_del_agua/', {
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
                alert("Se actualizaron las verificaciones correctamente.");
                return true;
            } else {
                alert("No se pudo actualizar las verificaciones.");
                return false;
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al verificar los registros.");
        }
    });
});