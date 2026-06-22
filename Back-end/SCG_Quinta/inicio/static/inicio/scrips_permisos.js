// Configuración global de jQuery para incluir CSRF en todas las peticiones POST/AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("submit", async function(event) {
        event.preventDefault();

        try {
            const userData = [];

            document.querySelectorAll('.usuario').forEach(function(user) {
                const id = user.dataset.id;
                const name = user.querySelector('.nombre-usuario').innerText.trim();
                const isActive = user.querySelector('.check-activo').checked;
                const isStaff = user.querySelector('.check-staff').checked;

                userData.push({
                    id: id,
                    name: name,
                    isActive: isActive,
                    isStaff: isStaff
                });
            });

            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            const response = await fetch('/inicio/vista_permisos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ userData: userData })
            });

            const data = await response.json();

            if (response.ok && data.existe) {
                alert(`Se actualizaron ${data.actualizados} usuarios correctamente.`);
            } else {
                alert(data.error || "No se pudo actualizar los permisos.");
            }

        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al guardar los permisos.");
        }
    });
});