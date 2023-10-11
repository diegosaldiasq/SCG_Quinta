document.getElementById("miBoton").addEventListener("click", async function() {
    let rutEnBase = document.getElementById("rut").value;

    var response = await fetch('/login/vista_ingresa_rut/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Aquí deberías agregar el csrf token para Django si es necesario
        },
        body: JSON.stringify({ dato: rutEnBase })
    })
    var data = await response.json();
    if (data.existe) {
        alert("El rut existe en la base de datos.");
        return true;
    } else {
        alert("El rut NO existe en la base de datos.");
        return false;
    } 
});