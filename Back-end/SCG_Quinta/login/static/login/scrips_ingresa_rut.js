document.addEventListener("DOMContentLoaded", function() {
    let logic = false; // Declara la variable en un ámbito superior

    document.getElementById('oneClick').addEventListener('click', async function() { // Note el uso de "async"
        var rutEnWeb = document.getElementById('rut').value;
        
        try {
            let response = await fetch('/login/vista_ingresa_rut/'); // Espera a que la petición se complete
            let data = await response.json(); // Espera a que la respuesta se convierta a JSON

            var rutEnBase = data.map(item => item.rut_base);
            logic = rutEnBase.includes(rutEnWeb);

        } catch (error) {
            console.error("Error al obtener el rut:", error);
        }
    
        if (logic == true) {
            //window.location.href = "/login/pasword/";
            alert("El rut ingresado se encuentra en la base de datos");
        } else {
            alert("El rut ingresado no se encuentra en la base de datos");
        }   
    });
});