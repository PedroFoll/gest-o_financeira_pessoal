// dashboard.js — lógica do dashboard Andromeda
// Arquivo: pages/home/static/home/js/dashboard.js

// Dados injetados pelo servidor via window.dadosDashboard (home.html)
// Fallback vazio para evitar erros se variável não estiver definida
const dadosDashboard = window.dadosDashboard || {
  receitas: 0, despesas: 0, saldo: 0, movimentacoes: 0, metaMensal: 6000,
  meses: [], receitasMensais: [], despesasMensais: [], movMensais: [], lancamentos: [],
};

// =====================================================
// FORMATAÇÃO
// =====================================================
function formatarMoeda(valor) {
  return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

// =====================================================
// BARRAS DE PROGRESSO DOS CARDS (valores já renderizados no HTML)
// =====================================================
function renderizarBarrasProgresso() {
  const { receitas, despesas, saldo, movimentacoes, metaMensal } = dadosDashboard;

  const barReceitas = document.getElementById('bar-receitas');
  const barDespesas = document.getElementById('bar-despesas');
  const barSaldo    = document.getElementById('bar-saldo');
  const barMov      = document.getElementById('bar-mov');

  if (barReceitas) barReceitas.style.width = `${Math.min((receitas / (metaMensal || 1)) * 100, 100)}%`;
  if (barDespesas) barDespesas.style.width = `${receitas > 0 ? Math.min((despesas / receitas) * 100, 100) : 0}%`;
  if (barSaldo)    barSaldo.style.width    = `${Math.min((Math.max(saldo, 0) / (metaMensal || 1)) * 100, 100)}%`;
  if (barMov)      barMov.style.width      = `${Math.min((movimentacoes / 30) * 100, 100)}%`;

  // Saldo negativo muda cor do valor
  const elSaldo = document.getElementById('total-saldo');
  if (elSaldo && saldo < 0) elSaldo.style.color = '#FF66B2';
}

// =====================================================
// GRÁFICO DE BARRAS — Receitas x Despesas
// =====================================================
function renderizarGraficoBarras() {
  const ctx = document.getElementById('grafico-barras');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dadosDashboard.meses,
      datasets: [
        {
          label: 'Receitas',
          data: dadosDashboard.receitasMensais,
          backgroundColor: 'rgba(34, 197, 94, 0.75)',
          borderRadius: 6,
          borderSkipped: false,
        },
        {
          label: 'Despesas',
          data: dadosDashboard.despesasMensais,
          backgroundColor: 'rgba(255, 102, 178, 0.75)',
          borderRadius: 6,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            boxWidth: 12,
            boxHeight: 12,
            borderRadius: 4,
            useBorderRadius: true,
            font: { size: 12 },
            color: '#6C4F94',
          },
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${formatarMoeda(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#6C4F94', font: { size: 11 } },
        },
        y: {
          grid: { color: 'rgba(225, 225, 225, 0.8)' },
          ticks: {
            color: '#6C4F94',
            font: { size: 11 },
            callback: (v) => `R$ ${(v / 1000).toFixed(0)}k`,
          },
        },
      },
    },
  });
}

// =====================================================
// GRÁFICO DE LINHA — Movimentações
// =====================================================
function renderizarGraficoLinha() {
  const ctx = document.getElementById('grafico-linha');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: dadosDashboard.meses,
      datasets: [
        {
          label: 'Movimentações',
          data: dadosDashboard.movMensais,
          borderColor: '#6C4F94',
          backgroundColor: 'rgba(108, 79, 148, 0.1)',
          pointBackgroundColor: '#FF66B2',
          pointBorderColor: '#FF66B2',
          pointRadius: 5,
          pointHoverRadius: 7,
          borderWidth: 2.5,
          tension: 0.4,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            boxWidth: 12,
            boxHeight: 12,
            borderRadius: 4,
            useBorderRadius: true,
            font: { size: 12 },
            color: '#6C4F94',
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#6C4F94', font: { size: 11 } },
        },
        y: {
          grid: { color: 'rgba(225, 225, 225, 0.8)' },
          ticks: { color: '#6C4F94', font: { size: 11 }, stepSize: 5 },
          beginAtZero: true,
        },
      },
    },
  });
}

// =====================================================
// CALENDÁRIO
// =====================================================
const MESES_PT = [
  'Janeiro','Fevereiro','Março','Abril','Maio','Junho',
  'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'
];

let calData = { ano: new Date().getFullYear(), mes: new Date().getMonth() };

function renderizarCalendario() {
  const { ano, mes } = calData;
  const hoje = new Date();
  const primeiroDia = new Date(ano, mes, 1).getDay();
  const totalDias = new Date(ano, mes + 1, 0).getDate();

  document.getElementById('cal-title').textContent = `${MESES_PT[mes]} ${ano}`;

  const grid = document.getElementById('cal-grid');
  grid.innerHTML = '';

  // Células vazias antes do primeiro dia
  for (let i = 0; i < primeiroDia; i++) {
    const vazio = document.createElement('div');
    vazio.className = 'cal-day cal-day--empty';
    vazio.setAttribute('role', 'gridcell');
    grid.appendChild(vazio);
  }

  // Dias do mês
  for (let dia = 1; dia <= totalDias; dia++) {
    const celula = document.createElement('div');
    celula.className = 'cal-day';
    celula.setAttribute('role', 'gridcell');
    celula.textContent = dia;

    const ehHoje = (
      dia === hoje.getDate() &&
      mes === hoje.getMonth() &&
      ano === hoje.getFullYear()
    );
    if (ehHoje) celula.classList.add('cal-day--today');

    grid.appendChild(celula);
  }
}

function inicializarCalendario() {
  document.getElementById('cal-prev')?.addEventListener('click', () => {
    calData.mes--;
    if (calData.mes < 0) { calData.mes = 11; calData.ano--; }
    renderizarCalendario();
  });

  document.getElementById('cal-next')?.addEventListener('click', () => {
    calData.mes++;
    if (calData.mes > 11) { calData.mes = 0; calData.ano++; }
    renderizarCalendario();
  });

  renderizarCalendario();
}

// =====================================================
// INIT
// =====================================================
document.addEventListener('DOMContentLoaded', () => {
  renderizarBarrasProgresso();
  renderizarGraficoBarras();
  renderizarGraficoLinha();
  inicializarCalendario();
});
