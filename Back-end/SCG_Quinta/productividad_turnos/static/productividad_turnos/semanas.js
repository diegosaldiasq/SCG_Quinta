(() => {
  'use strict';
  const form = document.getElementById('form-semana');
  if (!form) return;
  const format = n => n.toLocaleString('es-CL', { maximumFractionDigits: 0 });
  const update = () => {
    let count = 0, total = 0;
    form.querySelectorAll('.week-table tbody tr').forEach(row => {
      let dayTotal = 0;
      row.querySelectorAll('.week-cell').forEach(cell => {
        const active = cell.querySelector('input[name$="-programado"]');
        const input = cell.querySelector('input[name$="-meta_pt"]');
        if (active && active.checked) {
          count += 1;
          const value = input && input.value.trim() !== '' ? Number(input.value) : 0;
          if (Number.isFinite(value) && value >= 0) dayTotal += value;
        }
      });
      const label = row.querySelector('[data-day-total]');
      if (label) label.textContent = 'Meta del día: ' + format(dayTotal);
      total += dayTotal;
    });
    document.getElementById('week-turn-count').textContent = format(count);
    document.getElementById('week-target-total').textContent = format(total);
  };
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  update();
})();
