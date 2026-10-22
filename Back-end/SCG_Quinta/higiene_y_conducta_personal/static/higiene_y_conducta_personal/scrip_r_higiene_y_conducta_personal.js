document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-higiene");
    const tbody = document.getElementById("tbody-registros");
    const agregar = document.getElementById("btn-agregar-fila");
    const guardar = document.getElementById("miBoton");
    const fieldset = document.getElementById("campos-registros");
    const estado = document.getElementById("estado-guardado");
    const contador = document.getElementById("contador-registros");
    const plantilla = tbody.querySelector(".fila-registro").cloneNode(true);
    let guardando = false;

    function renumerarFilas() {
        const filas = tbody.querySelectorAll(".fila-registro");
        filas.forEach((fila, index) => {
            fila.querySelector(".num-registro").textContent = index + 1;
            const eliminar = fila.querySelector(".btn-eliminar-fila");
            eliminar.disabled = filas.length === 1;
            eliminar.setAttribute("aria-label", `Eliminar registro ${index + 1}`);
            fila.querySelectorAll("[data-campo]").forEach(campo => {
                campo.id = `${campo.dataset.campo}-${index + 1}`;
                campo.setAttribute("aria-label", `${campo.dataset.etiqueta}, fila ${index + 1}`);
            });
        });
        contador.textContent = `${filas.length} ${filas.length === 1 ? "registro" : "registros"}`;
    }

    function mostrarEstado(mensaje, error = false) {
        estado.textContent = mensaje;
        estado.classList.toggle("error", error);
    }

    agregar.addEventListener("click", function () {
        if (guardando) return;
        const fila = plantilla.cloneNode(true);
        tbody.appendChild(fila);
        renumerarFilas();
        fila.querySelector("[data-campo]").focus();
        mostrarEstado("");
    });

    tbody.addEventListener("click", function (event) {
        const eliminar = event.target.closest(".btn-eliminar-fila");
        if (!eliminar || guardando || tbody.rows.length === 1) return;
        eliminar.closest(".fila-registro").remove();
        renumerarFilas();
        mostrarEstado("");
    });

    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        if (guardando || !form.reportValidity()) return;

        const filas = Array.from(tbody.querySelectorAll(".fila-registro"));
        const datos = filas.map(fila => {
            const dato = {};
            fila.querySelectorAll("[data-campo]").forEach(campo => {
                dato[campo.dataset.campo] = campo.value.trim();
            });
            return dato;
        });
        const nombreVacio = datos.findIndex(dato => !dato.nombre_personal);
        if (nombreVacio !== -1) {
            mostrarEstado(`Completa el nombre del colaborador en la fila ${nombreVacio + 1}.`, true);
            filas[nombreVacio].querySelector('[data-campo="nombre_personal"]').focus();
            return;
        }

        guardando = true;
        fieldset.disabled = true;
        guardar.textContent = "Guardando…";
        form.setAttribute("aria-busy", "true");
        mostrarEstado(`Guardando ${datos.length} ${datos.length === 1 ? "registro" : "registros"}…`);
        try {
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
                },
                body: JSON.stringify({ datos })
            });
            // Una sesión expirada devuelve el HTML de inicio de sesión.
            if (response.redirected || !response.headers.get("content-type")?.includes("application/json")) {
                throw new Error("No se pudo confirmar el guardado. Revisa tu conexión y que tu sesión siga activa. Los datos siguen en pantalla.");
            }
            const data = await response.json();
            if (!response.ok || !data.existe) {
                throw new Error(data.error || "No se pudieron guardar los registros. Revisa los datos e intenta nuevamente.");
            }
            tbody.replaceChildren(plantilla.cloneNode(true));
            renumerarFilas();
            mostrarEstado(`${data.guardados} ${data.guardados === 1 ? "registro guardado" : "registros guardados"} correctamente.`);
        } catch (error) {
            const mensaje = error instanceof TypeError
                ? "No se pudo confirmar el guardado. Revisa tu conexión. Los datos siguen en pantalla."
                : error.message || "No se pudo confirmar el guardado. Los datos siguen en pantalla.";
            mostrarEstado(mensaje, true);
        } finally {
            guardando = false;
            fieldset.disabled = false;
            guardar.textContent = "Grabar y continuar";
            form.removeAttribute("aria-busy");
        }
    });

    renumerarFilas();
});