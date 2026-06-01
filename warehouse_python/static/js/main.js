// Warehouse Dashboard — main.js
// Shared JavaScript functions

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-hide alerts after 5 s ──────────────────────────────────────
  document.querySelectorAll('.alert.alert-success, .alert.alert-warning').forEach(el => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    }, 5000);
  });

  // ── Confirm dialogs for delete buttons (data-confirm attr) ──────────
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm)) e.preventDefault();
    });
  });

  // ── File input preview ───────────────────────────────────────────────
  document.querySelectorAll('input[type="file"][data-preview]').forEach(input => {
    const previewId = input.dataset.preview;
    const preview = document.getElementById(previewId);
    if (!preview) return;
    input.addEventListener('change', () => {
      const file = input.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = e => { preview.src = e.target.result; preview.style.display = 'block'; };
      reader.readAsDataURL(file);
    });
  });

});
