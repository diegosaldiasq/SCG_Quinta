document.addEventListener("DOMContentLoaded", function() {
    // Tu código JavaScript aquí
    const rutEnWeb = document.getElementById('rut').value;

    document.getElementById('miBoton').addEventListener('click', function() {
        fetch('/login/vista_ingresa_rut/') // Ruta a tu vista Django
            .then(response => response.json())
            .then(data => {
                const rutEnBase = data.map(item => item.rut_base);
                rutEnWeb = document.getElementById('rut').value;
    
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