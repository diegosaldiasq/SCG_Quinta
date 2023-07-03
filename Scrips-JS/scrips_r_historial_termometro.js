const valor1 = document.getElementById('valor1');
const valor2 = document.getElementById('valor2');
const valor3 = document.getElementById('valor3');
const valor4 = document.getElementById('valor4');
const valor5 = document.getElementById('valor5');
const output1 = document.getElementById('outputx1');

const valor6 = document.getElementById('valor6');
const valor7 = document.getElementById('valor7');
const valor8 = document.getElementById('valor8');
const valor9 = document.getElementById('valor9');
const valor10 = document.getElementById('valor10');
const output2 = document.getElementById('outputx2');

const factan = document.getElementById('factan');
const output3 = document.getElementById('outputx3');
const output4 = document.getElementById('outputx4');
const regla = document.getElementById('regla');

function btnOnClick() {
    const sumaCantidad1 = (Number(valor1.value) + Number(valor2.value) + Number(valor3.value) + Number(valor4.value) + Number(valor5.value))/5;
    output1.innerText = sumaCantidad1.toFixed(1);
}

function btnOnClick2() {
    const sumaCantidad2 = (Number(valor6.value) + Number(valor7.value) + Number(valor8.value) + Number(valor9.value) + Number(valor10.value))/5;
    output2.innerText = sumaCantidad2.toFixed(1);
}

function btnOnClick3() {
    const promedioCantidad = (((Number(valor1.value) + Number(valor2.value) + Number(valor3.value) + Number(valor4.value) + Number(valor5.value))/5) + ((Number(valor6.value) + Number(valor7.value) + Number(valor8.value) + Number(valor9.value) + Number(valor10.value))/5))/2;
    output3.innerText = promedioCantidad.toFixed(1);
    const x1 = ((Number(valor1.value) + Number(valor2.value) + Number(valor3.value) + Number(valor4.value) + Number(valor5.value))/5) - ((Number(valor6.value) + Number(valor7.value) + Number(valor8.value) + Number(valor9.value) + Number(valor10.value))/5) + Number(factan.value);
    // hacer un condicional
    output4.innerText = x1.toFixed(1);
    if (x1 >= -0.5 && x1 <= 0.5) {
        regla.innerText = 'Cumple';
    } else {
        regla.innerText = 'No cumple';
    }
}
