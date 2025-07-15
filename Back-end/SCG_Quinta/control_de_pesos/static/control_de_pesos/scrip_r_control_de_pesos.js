// Configuración global de jQuery para incluir CSRF en todas las peticiones POST/AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
     // 1) Restaurar lote y turno guardados en sessionStorage
    const campos = ['cliente','producto','codigo','peso','lote','turno'];
    campos.forEach(key => {
        const val = sessionStorage.getItem(key);
        if (val !== null) {
        const el = document.getElementById(
            key === 'pesoReal' ? 'peso-real' : key
        );
        if (el) el.value = val;
        // para <select> de cliente/turno
        if (el && el.tagName === 'SELECT') el.value = val;
        sessionStorage.removeItem(key);
        }
    });

    // 2) Listeners para guardar estado al cambiar campos
    // Cliente → repuebla producto y guarda cliente
    document.getElementById('cliente').addEventListener('change', () => {
        sessionStorage.setItem('cliente', this.value);
        // (reutiliza tu función de JS para repoblar productos)
    });

    // Producto → guarda producto, código y peso receta
    document.getElementById('producto').addEventListener('change', () => {
        const sel = this.selectedOptions[0];
        const codigo = sel?.dataset.codigo || '';
        const peso   = sel?.dataset.peso   || '';
        document.getElementById('codigo').value = codigo;
        document.getElementById('peso').value   = peso;
        sessionStorage.setItem('producto', sel.value);
        sessionStorage.setItem('codigo',   codigo);
        sessionStorage.setItem('peso',     peso);
    });

    // Lote y turno
    document.getElementById('lote').addEventListener('input', function() {
        sessionStorage.setItem('lote', this.value);
    });
    document.getElementById('turno').addEventListener('change', function() {
        sessionStorage.setItem('turno', this.value);
    });

    // 2) Listener para el botón
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var cliente = $("#cliente").val();
            var codigoProducto = $("#codigo").val();
            var producto = $("#producto").val();
            var pesoReceta = $("#peso").val();
            var pesoReal = $("#peso-real").val();
            var lote = $("#lote").val();
            var turno = $("#turno").val();

            // agregar valores a datos

            var datos = {
                cliente: cliente,
                producto: producto,
                codigo_producto: codigoProducto,
                peso_receta: pesoReceta,
                peso_real: pesoReal,
                lote: lote,
                turno: turno
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/control_de_pesos/vista_control_de_pesos/', {
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
                 // guardamos lote y turno en sessionStorage
                sessionStorage.setItem('lote', lote);
                sessionStorage.setItem('turno', turno);

                alert("Datos guardados exitosamente!!");
                location.reload();
            } else {
                alert("No se pudo guardar... revisa nuevamente!!");
                return false;
            }
        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al cargar los datos, formatos no coinciden!!");
        }
    });
});