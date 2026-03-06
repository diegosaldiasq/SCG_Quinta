document.addEventListener("DOMContentLoaded", function () {
    const clienteSelect = document.getElementById("id_cliente");
    const productoSelect = document.getElementById("id_producto");
    const codigoInput = document.getElementById("id_codigo_producto");
    const tablaBody = document.querySelector("#tablaIngredientes tbody");

    let proveedoresCache = [];

    async function cargarProveedores() {
        try {
            const response = await fetch("/trazabilidad_productos/ajax/proveedores/");
            const data = await response.json();
            proveedoresCache = data.proveedores || [];
        } catch (error) {
            console.error("Error cargando proveedores:", error);
            proveedoresCache = [];
        }
    }

    function construirOptionsProveedores() {
        let html = `<option value="">Seleccione proveedor</option>`;
        proveedoresCache.forEach((p) => {
            html += `<option value="${p.id}">${p.nombre}</option>`;
        });
        return html;
    }

    function resetearTabla(mensaje) {
        tablaBody.innerHTML = `
            <tr>
                <td colspan="6" class="texto-centro">${mensaje}</td>
            </tr>
        `;
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

            const proveedoresOptions = construirOptionsProveedores();

            ingredientes.forEach((ingrediente) => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>
                        ${ingrediente.nombre}
                        <input type="hidden" name="ingrediente_id[]" value="${ingrediente.id}">
                    </td>
                    <td><input type="text" name="lote[]" required></td>
                    <td><input type="date" name="fecha_elaboracion[]" required></td>
                    <td><input type="date" name="fecha_vencimiento[]" required></td>
                    <td>
                        <select name="proveedor[]" required>
                            ${proveedoresOptions}
                        </select>
                    </td>
                    <td><textarea name="accion_correctiva[]" rows="2"></textarea></td>
                `;
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
        await cargarProveedores();

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