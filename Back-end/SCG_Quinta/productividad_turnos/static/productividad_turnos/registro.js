(() => {
  'use strict';
  const form = document.getElementById('registro-form');
  if (!form) return;
  const output = document.getElementById('preview-calculos');
  const read = name => {
    const input = form.elements[name];
    if (!input || input.value.trim() === '') return null;
    const value = Number(input.value.replace(',', '.'));
    return Number.isFinite(value) ? value : null;
  };
  const format = (n, decimals = 2) => n === null ? '—' : n.toLocaleString('es-CL', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  const update = () => {
    const pt = read('terminadas'), people = read('dotacion'), hours = read('horas_persona');
    const target = Number(document.getElementById('meta-pt').dataset.meta);
    const cards = [
      ['Cumplimiento estimado', pt !== null && target > 0 ? format(pt / target * 100, 1) + ' %' : '—'],
      ['Unidades / persona', pt !== null && people > 0 ? format(pt / people) : '—'],
      ['Unidades / hora-persona', pt !== null && hours > 0 ? format(pt / hours) : '—'],
    ];
    output.replaceChildren(...cards.map(([label, value]) => {
      const div = document.createElement('div'), caption = document.createElement('span'), number = document.createElement('strong');
      caption.className = 'muted'; caption.textContent = label; number.textContent = value;
      div.append(caption, number); return div;
    }));
  };
  form.addEventListener('input', update);
  // No deshabilitar el botón antes del submit: su nombre identifica la acción en Django.
  update();
})();
