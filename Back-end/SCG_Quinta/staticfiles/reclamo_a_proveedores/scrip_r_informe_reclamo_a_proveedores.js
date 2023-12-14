/*document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    var nombreProveedor = document.getElementById('nombre-prov');
    var fechaReclamo = document.getElementById('fecha-recl');

    var nombreDelProducto = document.getElementById('nombre-prod');
    var fechaDeElaboracion = document.getElementById('fecha-elab');
    var lote = document.getElementById('lote');
    var fechaDeVencimiento = document.getElementById('fecha-venc');
    var noConformidad = document.getElementById('no-conf');

    var clasificacion = document.querySelector('clasificacion');
    var cantidadInvolucrada = document.querySelector('cantidad-inv');
    var unidadDeMedida = document.querySelector('udm')
    var archivoFoto = document.querySelector('archivo-foto');

    // Envio de datos a Django
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).ready(function() {
        $("#miBoton").click(function() {
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
            var archivoFoto = $("#archivo-foto").val();

            $.ajax({
                url: "/reclamo_a_proveedores/vista_reclamo_a_proveedores/",  // Ruta a tu vista Django
                method: "POST",
                data: {
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
                },
                success: function(response) {
                    // Hacer algo con la respuesta del servidor
                    console.log(response);
                    $("#mensaje").text(response.mensaje);
                },
            });
        });
    });
    // Fin de envio de datos a Django
});*/

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
            var archivoFoto = $("#archivo-foto").val();

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

            var response = await fetch('/reclamo_a_proveedores/vista_reclamo_a_proveedores/', {
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