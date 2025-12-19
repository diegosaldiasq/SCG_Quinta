// OJO: $.ajaxSetup NO afecta fetch(), solo afecta $.ajax.
// Como tu envío es con fetch(), no necesitas ajaxSetup para CSRF en este flujo.

// Si quieres dejarlo porque tienes otras llamadas $.ajax en otro lado, no molesta.
// Pero para este POST con fetch no aporta.
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {

    // =========================
    // 1) Seleccionar / deseleccionar todas
    // =========================
    const checkAll = document.getElementById('check_all_' + config);

    function getCheckboxes() {
        return document.querySelectorAll('.checkbox_' + config);
    }

    function syncCheckAllState() {
        if (!checkAll) return;
        const checkboxes = Array.from(getCheckboxes());
        if (checkboxes.length === 0) {
            checkAll.checked = false;
            checkAll.indeterminate = false;
            return;
        }

        const checkedCount = checkboxes.filter(c => c.checked).length;

        if (checkedCount === 0) {
            checkAll.checked = false;
            checkAll.indeterminate = false;
        } else if (checkedCount === checkboxes.length) {
            checkAll.checked = true;
            checkAll.indeterminate = false;
        } else {
            checkAll.checked = false;
            checkAll.indeterminate = true; // estado “mixto”
        }
    }

    if (checkAll) {
        checkAll.addEventListener('change', function () {
            const checkboxes = getCheckboxes();
            checkboxes.forEach(cb => {
                cb.checked = checkAll.checked;
            });
            checkAll.indeterminate = false;
        });
    }

    // Cuando cambie cualquiera, sincronizar el estado del master
    getCheckboxes().forEach(cb => {
        cb.addEventListener('change', syncCheckAllState);
    });

    // Estado inicial del master
    syncCheckAllState();

    // =========================
    // 2) Guardar cambios (POST)
    // =========================
    const form = document.getElementById('miBoton');

    if (form) {
        form.addEventListener('submit', async function (event) {
            try {
                event.preventDefault(); // no recargar

                const userData = [];

                // Opción A (recomendada): usar directamente los checkboxes y data-id
                const checkboxes = getCheckboxes();
                checkboxes.forEach(cb => {
                    userData.push({
                        id: cb.dataset.id,          // viene del template
                        isVerificado: cb.checked
                    });
                });

                // Obtener CSRF token del input hidden
                const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

                const response = await fetch('/inicio/verificar_registros/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ userData: userData })
                });

                const data = await response.json();

                if (data.existe) {
                    alert("Se actualizaron las verificaciones correctamente.");
                    window.location.reload();
                    return true;
                } else {
                    alert("No se pudo actualizar las verificaciones.");
                    return false;
                }

            } catch (error) {
                console.error("Hubo un error:", error);
                alert("Hubo un problema al verificar los registros.");
            }
        });
    }

});