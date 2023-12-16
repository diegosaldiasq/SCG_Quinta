document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var turno = $("#turno").val();
            var planta = $("#planta").val();
            var numeroLlave = $("#numero-llave").val();
            var puntoMuestreo = $("#punto-muestreo").val();
            var saborInsipido = $("#sabor-insipido").val();
            var olorInodora = $("#olor-inodora").val();
            var colorIcoloro = $("#color-incoloro").val();
            var ph = $("#ph").val();
            var cloroLibre = $("#cloro-libre").val();
            var accionCorrectiva = $("#ac").val();
            var resultadoAc = $("#resultado-ac").val();

            // agregar valores a datos

            var datos = {
                turno_mda: turno,
                planta_mda: planta,
                numero_llave: numeroLlave,
                punto_muestreo: puntoMuestreo,
                sabor_insipido: saborInsipido,
                olor_inodora: olorInodora,
                color_incoloro: colorIcoloro,
                ph_mda: ph,
                cloro_libre: cloroLibre,
                accion_correctiva: accionCorrectiva,
                resultado_ac: resultadoAc
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/monitoreo_del_agua/vista_monitoreo_del_agua/', {
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







