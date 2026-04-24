$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const loteInput = document.getElementById("lote");
    const turnoInput = document.getElementById("turno");
    const clienteInput = document.getElementById("cliente");
    const productoInput = document.getElementById("producto");
    const codigoInput = document.getElementById("codigo");
    const pesoRecetaInput = document.getElementById("peso");

    const tbodyMuestras = document.getElementById("tbody-muestras");
    const btnAgregarFila = document.getElementById("btn-agregar-fila");
    const btnGuardar = document.getElementById("miBoton");

    const loteGuardado = sessionStorage.getItem("lote");
    const turnoGuardado = sessionStorage.getItem("turno");

    if (loteGuardado !== null && loteInput) {
        loteInput.value = loteGuardado;
        sessionStorage.removeItem("lote");
    }

    if (turnoGuardado !== null && turnoInput) {
        turnoInput.value = turnoGuardado;
        sessionStorage.removeItem("turno");
    }

    function crearFilaMuestra(numero) {
        const tr = document.createElement("tr");
        tr.className = "fila-muestra";

        tr.innerHTML = `
            <td class="num-muestra">${numero}</td>
            <td>
                <input
                    type="number"
                    class="input input-peso-real"
                    min="0"
                    step="1"
                    placeholder="-"
                    required
                >
            </td>
            <td>
                <input
                    type="number"
                    class="input input-altura"
                    min="0"
                    step="1"
                    placeholder="-"
                >
            </td>
            <td>
                <button type="button" class="btn-eliminar-fila">Eliminar</button>
            </td>
        `;

        return tr;
    }

    function renumerarFilas() {
        const filas = tbodyMuestras.querySelectorAll(".fila-muestra");

        filas.forEach((fila, index) => {
            const celdaNumero = fila.querySelector(".num-muestra");
            const btnEliminar = fila.querySelector(".btn-eliminar-fila");

            if (celdaNumero) {
                celdaNumero.textContent = index + 1;
            }

            if (btnEliminar) {
                btnEliminar.disabled = filas.length === 1;
            }
        });
    }

    if (btnAgregarFila && tbodyMuestras) {
        btnAgregarFila.addEventListener("click", function () {
            const numero = tbodyMuestras.querySelectorAll(".fila-muestra").length + 1;
            const nuevaFila = crearFilaMuestra(numero);
            tbodyMuestras.appendChild(nuevaFila);
            renumerarFilas();
        });

        tbodyMuestras.addEventListener("click", function (e) {
            if (e.target.classList.contains("btn-eliminar-fila")) {
                const filas = tbodyMuestras.querySelectorAll(".fila-muestra");

                if (filas.length > 1) {
                    const fila = e.target.closest(".fila-muestra");
                    if (fila) {
                        fila.remove();
                        renumerarFilas();
                    }
                }
            }
        });

        renumerarFilas();
    }

    if (btnGuardar) {
        btnGuardar.addEventListener("click", async function (event) {
            event.preventDefault();

            try {
                const cliente = clienteInput ? clienteInput.value : "";
                const codigoProducto = codigoInput ? codigoInput.value : "";
                const producto = productoInput ? productoInput.value : "";
                const pesoReceta = pesoRecetaInput ? pesoRecetaInput.value : "";
                const lote = loteInput ? loteInput.value : "";
                const turno = turnoInput ? turnoInput.value : "";

                if (!cliente) {
                    alert("Debes seleccionar un cliente.");
                    return;
                }

                if (!producto) {
                    alert("Debes seleccionar un producto.");
                    return;
                }

                if (!pesoReceta) {
                    alert("No se encontró el peso receta.");
                    return;
                }

                if (!lote) {
                    alert("Debes ingresar un lote.");
                    return;
                }

                if (!turno) {
                    alert("Debes seleccionar un turno.");
                    return;
                }

                const filas = tbodyMuestras.querySelectorAll(".fila-muestra");
                const muestras = [];

                for (const fila of filas) {
                    const pesoRealInput = fila.querySelector(".input-peso-real");
                    const alturaInput = fila.querySelector(".input-altura");

                    const pesoReal = pesoRealInput ? pesoRealInput.value.trim() : "";
                    const altura = alturaInput ? alturaInput.value.trim() : "";

                    if (pesoReal !== "") {
                        muestras.push({
                            peso_real: pesoReal,
                            altura: altura
                        });
                    }
                }

                if (muestras.length === 0) {
                    alert("Debes ingresar al menos una muestra de peso.");
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

                const csrfTokenInput = document.querySelector("[name=csrfmiddlewaretoken]");
                const csrfToken = csrfTokenInput ? csrfTokenInput.value : csrftoken;

                const response = await fetch("/control_de_pesos_insumos_kuchen/vista_control_de_pesos_insumos_kuchen/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken
                    },
                    body: JSON.stringify({ dato: datos })
                });

                const data = await response.json();

                if (data.ok || data.existe) {
                    sessionStorage.setItem("lote", lote);
                    sessionStorage.setItem("turno", turno);
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
    }
});