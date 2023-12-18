document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var nombreProveedor = $("#nombre-prov").val();
            var fechaReclamo = $("#fecha-recl").val();
            var nombreDelProducto = $("#nombre-prod").val();
            var fechaDeElaboracion = $("#fecha-elab").val();
            var lote = $("#lote").val();
            var fechaDeVencimiento = $("#fecha-venc").val();
            var noConformidad = $("#no-conf").val();
            var clasificacion = $("#clasificacion").val();
            var cantidadInvolucrada = $("#cantidad-inv").val();
            var unidadDeMedida = $("#udm").val();
            var archivoFoto = document.getElementById('archivo-foto').files[0]; // Objeto File

            // agregar valores a datos

            var datos = {
                nombre_proveedor: nombreProveedor,
                fecha_reclamo: fechaReclamo,
                nombre_del_producto: nombreDelProducto,
                fecha_elaboracion: fechaDeElaboracion,
                lote: lote,
                fecha_vencimiento: fechaDeVencimiento,
                no_conformidad: noConformidad,
                clasificacion: clasificacion,
                cantidad_involucrada: cantidadInvolucrada,
                unidad_de_medida: unidadDeMedida,
                archivo_foto: archivoFoto
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var formData = new FormData();
            formData.append('dato', new Blob([JSON.stringify(datos)], {type: "application/json"}));
            formData.append('archivo_foto', archivoFoto); // archivoFoto debe ser un objeto File

            var response = await fetch('/reclamo_a_proveedores/vista_reclamo_a_proveedores/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
                },
                body: formData
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