const nombreTecnologo = document.getElementById('nombre-tecnologo');
const fechaRegistro = document.getElementById('fecha-reg');

const codigoTermometro = document.getElementById('codigo-termometro');
const valor1 = document.getElementById('valor1');
const valor2 = document.getElementById('valor2');
const valor3 = document.getElementById('valor3');
const valor4 = document.getElementById('valor4');
const valor5 = document.getElementById('valor5');
var output1 = document.getElementById('outputx1');

const valor6 = document.getElementById('valor6');
const valor7 = document.getElementById('valor7');
const valor8 = document.getElementById('valor8');
const valor9 = document.getElementById('valor9');
const valor10 = document.getElementById('valor10');
var output2 = document.getElementById('outputx2');

const factan = document.getElementById('factan');
const output3 = document.getElementById('outputx3');
const output4 = document.getElementById('outputx4');
const regla = document.getElementById('regla');
const accionCorrectiva = document.getElementById('ac');
const verificacionAccionCorrectiva = document.getElementById('vac');


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
$(document).ready(function() {
    $("#miBoton").click(function() {

        $.ajax({
            url: "vista_historial_termometro",  // Ruta a tu vista Django
            method: "POST",
            data: {
                nombre_tecnologo: nombreTecnologo,
                fecha_registro: fechaRegistro,
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
                promedio_termometros: informacionFunction.promedioCantidad,
                nivel_aceptacion: informacionFunction.x1,
                cumplimiento: informacionFunction.regla,
                accion_correctiva: accionCorrectiva,
                verificacion_accion_correctiva: verificacionAccionCorrectiva
            },
            success: function(response) {
                // Hacer algo con la respuesta del servidor
                console.log(response);
            },
            error: function() {
                // Manejar errores
            }
        });
    });
});

//console.log(informacionFunction.promedioCantidad);
//console.log(informacionFunction.x1);
//console.log(informacionFunction.regla);