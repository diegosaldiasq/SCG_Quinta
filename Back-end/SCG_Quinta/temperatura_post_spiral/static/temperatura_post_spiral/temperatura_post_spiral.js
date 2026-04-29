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