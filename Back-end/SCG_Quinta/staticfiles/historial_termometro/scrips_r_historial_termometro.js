// Funciones para el registro de historial de termometro
var codigoTermometro = document.getElementById('codigo-termometro');
var valor1 = document.getElementById('valor1');
var valor2 = document.getElementById('valor2');
var valor3 = document.getElementById('valor3');
var valor4 = document.getElementById('valor4');
var valor5 = document.getElementById('valor5');
var output1 = document.getElementById('outputx1');

var valor6 = document.getElementById('valor6');
var valor7 = document.getElementById('valor7');
var valor8 = document.getElementById('valor8');
var valor9 = document.getElementById('valor9');
var valor10 = document.getElementById('valor10');
var output2 = document.getElementById('outputx2');

var factan = document.getElementById('factan');
var output3 = document.getElementById('outputx3');
var output4 = document.getElementById('outputx4');
var regla = document.getElementById('regla');
var accionCorrectiva = document.getElementById('ac');
var verificacionAccionCorrectiva = document.getElementById('vac');


// funcion para ver promedio de ingreso de termometro de muestra
function btnOnClick() {
    const sumaCantidad1 = (Number(valor1.value) + Number(valor2.value) + Number(valor3.value) + Number(valor4.value) + Number(valor5.value))/5;
    output1.innerText = sumaCantidad1.toFixed(1);
    return output1 = sumaCantidad1;
}

// funcion para ver promedio de ingreso de termometro patron
function btnOnClick2() {
    const sumaCantidad2 = (Number(valor6.value) + Number(valor7.value) + Number(valor8.value) + Number(valor9.value) + Number(valor10.value))/5;
    output2.innerText = sumaCantidad2.toFixed(1);
    return output2 = sumaCantidad2;
}

// funcion para ver promedio de ambos termometros, factor de correccion y regla
var informacionFunction = {};
function btnOnClick3() {
    var reglaLog = 'Vacio';
    const promedioCantidad = (((Number(valor1.value) + Number(valor2.value) + Number(valor3.value) + Number(valor4.value) + Number(valor5.value))/5) + ((Number(valor6.value) + Number(valor7.value) + Number(valor8.value) + Number(valor9.value) + Number(valor10.value))/5))/2;
    output3.innerText = promedioCantidad.toFixed(1);
    const x1 = ((Number(valor1.value) + Number(valor2.value) + Number(valor3.value) + Number(valor4.value) + Number(valor5.value))/5) - ((Number(valor6.value) + Number(valor7.value) + Number(valor8.value) + Number(valor9.value) + Number(valor10.value))/5) + Number(factan.value);
    output4.innerText = x1.toFixed(1);
    if (x1 >= -0.5 && x1 <= 0.5) {
        regla.innerText = 'Cumple';
        reglaLog = 'Cumple';
    } else {
        regla.innerText = 'No cumple';
        reglaLog = 'No cumple';
    }

    var informacion = {
        promedioCantidad: promedioCantidad,
        x1: x1,
        regla: reglaLog
    };

    return informacionFunction = informacion;
}


// envio de datos a django

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("miBoton").addEventListener("click", async function() {
        try {
            event.preventDefault(); // <-- para no recargar la pagina al enviar el formulario
            var codigoTermometro = $("#codigo-termometro").val();
            var valor1 = $("#valor1").val();
            var valor2 = $("#valor2").val();
            var valor3 = $("#valor3").val();
            var valor4 = $("#valor4").val();
            var valor5 = $("#valor5").val();
            var output1 = $("#outputx1").val();
            var valor6 = $("#valor6").val();
            var valor7 = $("#valor7").val();
            var valor8 = $("#valor8").val();
            var valor9 = $("#valor9").val();
            var valor10 = $("#valor10").val();
            var output2 = $("#outputx2").val();
            var factan = $("#factan").val();
            var output3 = $("#outputx3").val();
            var output4 = $("#outputx4").val();
            var regla = $('#regla').val();
            var accionCorrectiva = $("#ac").val();
            var verificacionAccionCorrectiva = $("#vac").val();

            // agregar valores a datos

            var datos = {
                codigo_termometro: codigoTermometro,
                valor_1: valor1,
                valor_2: valor2,
                valor_3: valor3,
                valor_4: valor4,
                valor_5: valor5,
                promedio_prueba: output1,
                valor_6: valor6,
                valor_7: valor7,
                valor_8: valor8,
                valor_9: valor9,
                valor_10: valor10,
                promedio_patron: output2,
                factor_anual: factan,
                promedio_termometros: output3,
                nivel_aceptacion: output4,
                cumplimiento: regla,
                accion_correctiva: accionCorrectiva,
                verificacion_accion_correctiva: verificacionAccionCorrectiva
            }
            
            // Obtener el CSRF token
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            var response = await fetch('/historial_termometro/vista_historial_termometro/', {
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