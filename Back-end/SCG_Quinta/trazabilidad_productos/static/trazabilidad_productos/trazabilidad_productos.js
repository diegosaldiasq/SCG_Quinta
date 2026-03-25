document.addEventListener("DOMContentLoaded", function () {
    const clienteSelect = document.getElementById("id_cliente");
    const productoSelect = document.getElementById("id_producto");
    const codigoInput = document.getElementById("id_codigo_producto");
    const tablaBody = document.querySelector("#tablaIngredientes tbody");

    function resetearTabla(mensaje) {
        tablaBody.innerHTML = `
            <tr>
                <td colspan="7" class="texto-centro">${mensaje}</td>
            </tr>
        `;
    }

    function crearFilaIngrediente(ingrediente, esDuplicada = false) {
        const fila = document.createElement("tr");
        fila.classList.add("fila-ingrediente");

        fila.innerHTML = `
            <td>
                ${ingrediente.nombre}
                ${esDuplicada ? '<div class="subtexto">Lote adicional</div>' : ''}
                <input type="hidden" name="ingrediente_id[]" value="${ingrediente.id}">
                <input type="hidden" name="proveedor_id[]" value="${ingrediente.proveedor_id}">
            </td>

            <td>
                <input type="text" name="lote[]" required>
            </td>

            <td>
                <input type="date" name="fecha_elaboracion[]" required>
            </td>

            <td>
                <input type="date" name="fecha_vencimiento[]" required>
            </td>

            <td>
                ${ingrediente.proveedor_nombre || "Sin proveedor"}
            </td>

            <td>
                <textarea name="accion_correctiva[]" rows="2"></textarea>
            </td>

            <td>
                <div class="acciones-fila">
                    <button type="button" class="btn-mini btn-agregar-lote">+ Lote</button>
                    ${
                        esDuplicada
                            ? '<button type="button" class="btn-mini btn-eliminar-fila">Eliminar</button>'
                            : ''
                    }
                </div>
            </td>
        `;

        const btnAgregar = fila.querySelector(".btn-agregar-lote");
        btnAgregar.addEventListener("click", function () {
            const nuevaFila = crearFilaIngrediente(ingrediente, true);
            fila.insertAdjacentElement("afterend", nuevaFila);
        });

        const btnEliminar = fila.querySelector(".btn-eliminar-fila");
        if (btnEliminar) {
            btnEliminar.addEventListener("click", function () {
                fila.remove();
            });
        }

        return fila;
    }

    async function cargarProductosPorCliente(clienteId, productoSeleccionado = "") {
        productoSelect.innerHTML = `<option value="">Seleccione producto</option>`;
        codigoInput.value = "";
        resetearTabla("Seleccione un producto para cargar sus ingredientes");

        if (!clienteId) return;

        try {
            const response = await fetch(`/trazabilidad_productos/ajax/productos/?cliente_id=${clienteId}`);
            const data = await response.json();

            (data.productos || []).forEach((producto) => {
                const option = document.createElement("option");
                option.value = producto.id;
                option.textContent = producto.nombre;
                option.dataset.codigo = producto.codigo;

                if (String(producto.id) === String(productoSeleccionado)) {
                    option.selected = true;
                }

                productoSelect.appendChild(option);
            });

            if (productoSeleccionado) {
                productoSelect.dispatchEvent(new Event("change"));
            }
        } catch (error) {
            console.error("Error cargando productos:", error);
        }
    }

    async function cargarIngredientesPorProducto(productoId) {
        tablaBody.innerHTML = "";

        if (!productoId) {
            resetearTabla("Seleccione un producto para cargar sus ingredientes");
            return;
        }

        try {
            const response = await fetch(`/trazabilidad_productos/ajax/ingredientes/?producto_id=${productoId}`);
            const data = await response.json();

            const ingredientes = data.ingredientes || [];

            if (ingredientes.length === 0) {
                resetearTabla("Este producto no tiene ingredientes configurados");
                return;
            }

            ingredientes.forEach((ingrediente) => {
                const fila = crearFilaIngrediente(ingrediente, false);
                tablaBody.appendChild(fila);
            });
        } catch (error) {
            console.error("Error cargando ingredientes:", error);
            resetearTabla("Ocurrió un error al cargar los ingredientes");
        }
    }

    if (clienteSelect) {
        clienteSelect.addEventListener("change", function () {
            cargarProductosPorCliente(this.value);
        });
    }

    if (productoSelect) {
        productoSelect.addEventListener("change", function () {
            const selectedOption = this.options[this.selectedIndex];
            codigoInput.value = selectedOption?.dataset?.codigo || "";
            cargarIngredientesPorProducto(this.value);
        });
    }

    async function inicializarFormulario() {
        if (clienteSelect) {
            const clienteSeleccionado = clienteSelect.value;
            const productoSeleccionado = productoSelect?.dataset?.selected || "";

            if (clienteSeleccionado) {
                await cargarProductosPorCliente(clienteSeleccionado, productoSeleccionado);
            }
        }
    }

    inicializarFormulario();
});