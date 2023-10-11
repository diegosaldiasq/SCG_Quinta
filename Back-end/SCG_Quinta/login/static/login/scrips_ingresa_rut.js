document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('miBoton').addEventListener('click', async function() {
        var rutEnWeb = document.getElementById('rut').value;
        var response = await fetch('/login/vista_ingresa_rut/'); // Ruta a tu vista Django
        var data = await response.json();    
        var rutEnBase = await data.map(item => item.rut_base);
        console.log(rutEnBase, rutEnWeb);
        if (rutEnBase.includes(rutEnWeb)) {
            //window.location.href = "/login/pasword/";
            alert("El rut ingresado se encuentra en la base de datos");
            return true;
        } else {
            alert("El rut ingresado no se encuentra en la base de datos");
            return false;
        }   
    });
});