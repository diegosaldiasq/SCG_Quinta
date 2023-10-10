document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('miBoton').addEventListener('click', function() {
        const rutEnWeb = document.getElementById('rut').value;
        fetch('/login/vista_ingresa_rut/') // Ruta a tu vista Django
            .then(response => response.json())
            .then(data => {
                const rutEnBase = data.map(item => item.rut_base);
                console.log(rutEnBase, rutEnWeb);
                if (rutEnBase.includes(rutEnWeb)) {
                    //window.location.href = "/login/pasword/";
                    alert("El rut ingresado se encuentra en la base de datos");
                    return true;
                } else {
                    alert("El rut ingresado no se encuentra en la base de datos");
                    return false;
                }
            })
            .catch(error => console.error('Error:', error));
    });
});