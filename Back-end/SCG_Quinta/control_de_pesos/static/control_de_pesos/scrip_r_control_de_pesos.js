// Configuración global de jQuery para incluir CSRF en todas las peticiones POST/AJAX
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const loteInput = document.getElementById('lote');
    const turnoInput = document.getElementById('turno');
    const tbodyMuestras = document.getElementById('tbody-muestras');
    const btnAgregarFila = document.getElementById('btn-agregar-fila');
    const btnGuardar = document.getElementById("miBoton");

    // Restaurar lote y turno
    const loteGuardado = sessionStorage.getItem('lote');
    const turnoGuardado = sessionStorage.getItem('turno');

    if (loteGuardado !== null && loteInput) {
        loteInput.value = loteGuardado;
        sessionStorage.removeItem('lote');
    }

    if (turnoGuardado !== null && turnoInput) {
        turnoInput.value = turnoGuardado;
        sessionStorage.removeItem('turno');
    }

    function renumerarFilas() {
        const filas = tbodyMuestras.querySelectorAll('.fila-muestra');
        filas.forEach((fila, index) => {
            const celdaNumero = fila.querySelector('.num-muestra');
            if (celdaNumero) {
                celdaNumero.textContent = index + 1;
            }

            const btnEliminar = fila.querySelector('.btn-eliminar-fila');
            if (btnEliminar) {
                btnEliminar.disabled = filas.length === 1;
            }
        });
    }

    function crearFila() {
        const tr = document.createElement('tr');
        tr.className = 'fila-muestra';
        tr.innerHTML = `
            <td class="num-muestra"></td>
            <td>
                <input type="number" class="input-peso-real" step="1" min="0" required>
            </td>
            <td>
                <input type="number" class="input-altura" step="0.1" min="0">
            </td>
            <td>
                <button type="button" class="btn-eliminar-fila">Eliminar</button>
            </td>
        `;
        return tr;
    }

    btnAgregarFila.addEventListener('click', function () {
        const nuevaFila = crearFila();
        tbodyMuestras.appendChild(nuevaFila);
        renumerarFilas();
    });

    tbodyMuestras.addEventListener('click', function (e) {
        if (e.target.classList.contains('btn-eliminar-fila')) {
            const filas = tbodyMuestras.querySelectorAll('.fila-muestra');
            if (filas.length > 1) {
                e.target.closest('.fila-muestra').remove();
                renumerarFilas();
            }
        }
    });

    renumerarFilas();

    btnGuardar.addEventListener("click", async function (event) {
        event.preventDefault();

        try {
            const cliente = $("#cliente").val();
            const codigoProducto = $("#codigo").val();
            const producto = $("#producto").val();
            const pesoReceta = $("#peso").val();
            const lote = $("#lote").val();
            const turno = $("#turno").val();

            const filas = tbodyMuestras.querySelectorAll('.fila-muestra');
            const muestras = [];

            filas.forEach((fila) => {
                const pesoReal = fila.querySelector('.input-peso-real')?.value;
                const altura = fila.querySelector('.input-altura')?.value;

                if (pesoReal !== "") {
                    muestras.push({
                        peso_real: pesoReal,
                        altura: altura
                    });
                }
            });

            if (!cliente || !producto || !pesoReceta || !lote || !turno) {
                alert("Debes completar cliente, producto, peso receta, lote y turno.");
                return;
            }

            if (muestras.length === 0) {
                alert("Debes ingresar al menos una muestra.");
                return;
            }

            const datos = {
                cliente: cliente,
                producto: producto,
                codigo_producto: codigoProducto,
                peso_receta: pesoReceta,
                lote: lote,
                turno: turno,
                muestras: muestras
            };

            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            const response = await fetch('/control_de_pesos/vista_control_de_pesos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ dato: datos })
            });

            const data = await response.json();

            if (data.ok) {
                sessionStorage.setItem('lote', lote);
                sessionStorage.setItem('turno', turno);
                alert(data.mensaje || "Datos guardados exitosamente.");
                location.reload();
            } else {
                alert(data.mensaje || "No se pudo guardar la información.");
            }

        } catch (error) {
            console.error("Hubo un error:", error);
            alert("Hubo un problema al guardar los datos.");
        }
    });
});