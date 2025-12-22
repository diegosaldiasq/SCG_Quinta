// Configuración global de jQuery para incluir CSRF en todas las peticiones POST/AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
document.getElementById("miBoton").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_' + config);

        datos.forEach(function(dato) {
            let id = dato.querySelector('span').innerText;
            let isVerificado = dato.querySelectorAll('input[type="checkbox"]')[0].checked;
    
            userData.push({
                id: id,
                isVerificado: isVerificado
            });
        });          
        // Obtener el CSRF token
        var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        var response = await fetch('/inicio/verificar_registros/', {
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
            alert("Se actualizaron las verificaciones correctamente.");
            window.location.reload(); // Esto recargará la página
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