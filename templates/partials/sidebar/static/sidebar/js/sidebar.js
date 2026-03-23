// sidebar.js — toggle da sidebar lateral
// Arquivo: partials/sidebar/static/sidebar/js/sidebar.js

const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

function abrirSidebar() {
  sidebar.classList.add('sidebar-open');
  sidebarOverlay.classList.add('active');
  sidebarToggle.setAttribute('aria-expanded', 'true');
  document.body.style.overflow = 'hidden';
}

function fecharSidebar() {
  sidebar.classList.remove('sidebar-open');
  sidebarOverlay.classList.remove('active');
  sidebarToggle.setAttribute('aria-expanded', 'false');
  document.body.style.overflow = '';
}

if (sidebarToggle) {
  sidebarToggle.addEventListener('click', () => {
    if (sidebar.classList.contains('sidebar-open')) {
      fecharSidebar();
    } else {
      abrirSidebar();
    }
  });
}

if (sidebarOverlay) {
  sidebarOverlay.addEventListener('click', fecharSidebar);
}

// Fechar sidebar com a tecla Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && sidebar && sidebar.classList.contains('sidebar-open')) {
    fecharSidebar();
  }
});
