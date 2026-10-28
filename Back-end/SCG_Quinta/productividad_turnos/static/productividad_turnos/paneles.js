(() => {
  'use strict';
  const dashboard = document.getElementById('dashboard');
  if (!dashboard) return;
  const status = document.getElementById('poll-status'), button = document.getElementById('actualizar-panel');
  let loading = false;
  const refresh = async () => {
    if (loading || document.hidden) return;
    loading = true; button.disabled = true;
    const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch(dashboard.dataset.api, { credentials: 'same-origin', headers: { 'Accept': 'application/json' }, signal: controller.signal });
      if (!response.ok || !response.headers.get('content-type')?.includes('application/json')) throw new Error('No disponible');
      const data = await response.json();
      // Fragmento renderizado por Django con autoescape, procedente de la misma aplicación.
      dashboard.innerHTML = data.html;
      status.textContent = 'Actualizado. Próxima consulta automática en 60 segundos.';
    } catch (_) {
      status.textContent = 'No se pudo actualizar. Revise la conexión o vuelva a iniciar sesión. Se conservan los datos visibles.';
    } finally {
      clearTimeout(timer); loading = false; button.disabled = false;
    }
  };
  button.addEventListener('click', refresh);
  setInterval(refresh, 60000);
})();
