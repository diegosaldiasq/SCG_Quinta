document.getElementById("miBoton_monitoreo_del_agua").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_monitoreo_del_agua');

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

document.getElementById("miBoton_higiene_y_conducta_personal").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_higiene_y_conducta_personal');

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

        var response = await fetch('/inicio/verificar_higiene_y_conducta_personal/', {
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

document.getElementById("miBoton_monitoreo_de_plagas").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_monitoreo_de_plagas');

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

        var response = await fetch('/inicio/verificar_monitoreo_de_plagas/', {
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

document.getElementById("miBoton_recepcion_mpme").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_recepcion_mpme');

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

        var response = await fetch('/inicio/verificar_recepcion_mpme/', {
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

document.getElementById("miBoton_pcc2_detector_metales").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_pcc2_detector_metales');

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

        var response = await fetch('/inicio/verificar_pcc2_detector_metales/', {
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

document.getElementById("miBoton_control_de_transporte").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_control_de_transporte');

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

        var response = await fetch('/inicio/verificar_control_de_transporte/', {
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

document.getElementById("miBoton_temperatura_despacho_ptjumbo").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_temperatura_despacho_ptjumbo');

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

        var response = await fetch('/inicio/verificar_temperatura_despacho_ptjumbo/', {
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

document.getElementById("miBoton_temperatura_despacho_ptsisa").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_temperatura_despacho_ptsisa');

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

        var response = await fetch('/inicio/verificar_temperatura_despacho_ptsisa/', {
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

document.getElementById("miBoton_historial_termometro").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_historial_termometro');

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

        var response = await fetch('/inicio/verificar_historial_termometro/', {
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

document.getElementById("miBoton_reclamo_a_proveedores").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_reclamo_a_proveedores');

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

        var response = await fetch('/inicio/verificar_reclamo_a_proveedores/', {
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

document.getElementById("miBoton_rechazo_mp_in_me").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_rechazo_mp_in_me');

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

        var response = await fetch('/inicio/verificar_rechazo_mp_in_me/', {
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

document.getElementById("miBoton_informe_de_incidentes").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_informe_de_incidentes');

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

        var response = await fetch('/inicio/verificar_informe_de_incidentes/', {
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

document.getElementById("miBoton_control_material_extraño").addEventListener("click", async function() {
    try {
        event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
        var userData = [];

        let datos = document.querySelectorAll('.usuario_control_material_extraño');

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

        var response = await fetch('/inicio/verificar_control_material_extraño/', {
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