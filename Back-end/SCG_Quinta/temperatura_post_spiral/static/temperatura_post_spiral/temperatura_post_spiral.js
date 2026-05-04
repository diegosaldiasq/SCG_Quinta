document.addEventListener("DOMContentLoaded", function () {
    const selectCliente = document.getElementById("id_cliente_selector");
    const selectProducto = document.getElementById("id_producto_sala_cremas");
    const codigoPreview = document.getElementById("codigo_producto_preview");

    if (!selectCliente || !selectProducto) return;

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
});

document.addEventListener("DOMContentLoaded", function () {
    const btnAgregar = document.getElementById("btn-agregar-linea");
    const tbody = document.getElementById("tbody-detalles");
    const totalForms = document.getElementById("id_detalles-TOTAL_FORMS");

    if (!btnAgregar || !tbody || !totalForms) return;

    function actualizarNumeros() {
        const filas = tbody.querySelectorAll(".fila-detalle");
        filas.forEach((fila, index) => {
            const numero = fila.querySelector(".numero-linea");
            if (numero) numero.textContent = index + 1;
        });
    }

    btnAgregar.addEventListener("click", function () {
        const formIndex = parseInt(totalForms.value);
        const primeraFila = tbody.querySelector(".fila-detalle");
        const nuevaFila = primeraFila.cloneNode(true);

        nuevaFila.querySelectorAll("input, textarea, select").forEach((input) => {
            if (input.name) {
                input.name = input.name.replace(/detalles-\d+-/g, `detalles-${formIndex}-`);
            }

            if (input.id) {
                input.id = input.id.replace(/id_detalles-\d+-/g, `id_detalles-${formIndex}-`);
            }

            if (input.type === "checkbox") {
                input.checked = false;
            } else if (input.type !== "hidden") {
                input.value = "";
            } else {
                input.value = "";
            }
        });

        tbody.appendChild(nuevaFila);
        totalForms.value = formIndex + 1;

        actualizarNumeros();
    });

    tbody.addEventListener("change", function (e) {
        if (e.target && e.target.name && e.target.name.includes("-DELETE")) {
            actualizarNumeros();
        }
    });
});