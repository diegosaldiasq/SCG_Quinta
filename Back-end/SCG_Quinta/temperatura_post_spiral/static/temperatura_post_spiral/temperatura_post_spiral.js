document.addEventListener("DOMContentLoaded", function () {
    const selectCliente = document.getElementById("id_cliente_selector");
    const selectProducto = document.getElementById("id_producto_sala_cremas");
    const codigoPreview = document.getElementById("codigo_producto_preview");

    if (selectCliente && selectProducto) {
        function limpiarProductos() {
            selectProducto.innerHTML = '<option value="">Seleccione producto</option>';
            if (codigoPreview) codigoPreview.value = "";
        }

        function cargarProductos(cliente) {
            limpiarProductos();

            if (!cliente) return;

            const url = `${window.URL_PRODUCTOS_POR_CLIENTE}?cliente=${encodeURIComponent(cliente)}`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    data.forEach(producto => {
                        const option = document.createElement("option");
                        option.value = producto.id;
                        option.textContent = producto.producto;
                        option.dataset.codigo = producto.codigo;
                        selectProducto.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("Error cargando productos:", error);
                });
        }

        selectCliente.addEventListener("change", function () {
            cargarProductos(this.value);
        });

        selectProducto.addEventListener("change", function () {
            const selected = selectProducto.options[selectProducto.selectedIndex];

            if (codigoPreview) {
                codigoPreview.value = selected.dataset.codigo || "";
            }
        });
    }

    const btnAgregar = document.getElementById("btn-agregar-linea");
    const tbody = document.getElementById("tbody-detalles");
    const totalForms = document.getElementById("id_detalles-TOTAL_FORMS");

    if (!btnAgregar || !tbody || !totalForms) return;

    const MIN_FILAS = 10;

    function renumerarFilas() {
        const filas = tbody.querySelectorAll(".fila-detalle");

        filas.forEach((fila, index) => {
            const numero = fila.querySelector(".numero-linea");
            if (numero) numero.textContent = index + 1;

            fila.querySelectorAll("input, textarea, select, label").forEach((el) => {
                if (el.name) {
                    el.name = el.name.replace(/detalles-\d+-/g, `detalles-${index}-`);
                }

                if (el.id) {
                    el.id = el.id.replace(/id_detalles-\d+-/g, `id_detalles-${index}-`);
                }

                if (el.htmlFor) {
                    el.htmlFor = el.htmlFor.replace(/id_detalles-\d+-/g, `id_detalles-${index}-`);
                }
            });
        });

        totalForms.value = filas.length;
    }

    function limpiarFila(fila) {
        fila.querySelectorAll("input, textarea, select").forEach((input) => {
            input.value = "";
        });
    }

    btnAgregar.addEventListener("click", function () {
        const primeraFila = tbody.querySelector(".fila-detalle");
        if (!primeraFila) return;

        const nuevaFila = primeraFila.cloneNode(true);
        limpiarFila(nuevaFila);

        tbody.appendChild(nuevaFila);
        renumerarFilas();
    });

    tbody.addEventListener("click", function (e) {
        const btnQuitar = e.target.closest(".btn-quitar-linea");
        if (!btnQuitar) return;

        const filas = tbody.querySelectorAll(".fila-detalle");

        if (filas.length <= MIN_FILAS) {
            alert("Debe mantener mínimo 10 registros de temperatura.");
            return;
        }

        const fila = btnQuitar.closest("tr");
        if (fila) {
            fila.remove();
            renumerarFilas();
        }
    });

    renumerarFilas();
});