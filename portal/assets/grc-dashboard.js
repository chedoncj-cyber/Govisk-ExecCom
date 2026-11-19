/* ── Animated counters ── */
  function animateCount(el, target, suffix, duration) {
    const start = performance.now();
    function step(now) {
      const t = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(ease * target) + suffix;
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  window.addEventListener('DOMContentLoaded', () => {
    animateCount(document.getElementById('gov-score'),     72, '%', 1200);
    animateCount(document.getElementById('risk-score'),    77, '%', 1200);
    animateCount(document.getElementById('comp-score'),    87, '%', 1200);
    animateCount(document.getElementById('overall-score'), 79, '%', 1200);

    /* Animate score bars */
    setTimeout(() => {
      document.querySelectorAll('.score-bar-fill[data-width]').forEach(el => {
        el.style.transition = 'width 1.2s ease';
        el.style.width = el.dataset.width;
      });
    }, 200);

    buildCharts();
    buildKPIs();
  });

  /* ── Chart.js defaults ── */
  Chart.defaults.color = '#94A3B8';
  Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif";
  Chart.defaults.font.size = 11;

  function buildCharts() {
    /* ── Radar ── */
    new Chart(document.getElementById('radarChart'), {
      type: 'radar',
      data: {
        labels: ['Board Oversight', 'Policy Docs', 'Risk Appetite', 'Risk Register', 'Reg Monitoring', 'Training', 'Control Effectiveness', 'Audit Findings'],
        datasets: [{
          label: 'Meridian Capital',
          data: [90, 78, 85, 82, 88, 91, 83, 80],
          backgroundColor: 'rgba(20,184,166,0.15)',
          borderColor: '#14B8A6',
          borderWidth: 2,
          pointBackgroundColor: '#14B8A6',
          pointRadius: 4,
        }, {
          label: 'Industry Benchmark',
          data: [75, 80, 78, 75, 80, 85, 78, 75],
          backgroundColor: 'rgba(59,130,246,0.08)',
          borderColor: 'rgba(59,130,246,0.4)',
          borderWidth: 1.5,
          borderDash: [4,4],
          pointRadius: 3,
          pointBackgroundColor: '#3B82F6',
        }]
      },
      options: {
        responsive: true,
        scales: {
          r: {
            min: 0, max: 100,
            ticks: { stepSize: 25, color: '#475569', font: { size: 9 } },
            grid: { color: 'rgba(255,255,255,0.06)' },
            angleLines: { color: 'rgba(255,255,255,0.06)' },
            pointLabels: { color: '#94A3B8', font: { size: 10 } },
          }
        },
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 10, padding: 12 } }
        }
      }
    });

    /* ── Trend Line ── */
    new Chart(document.getElementById('trendChart'), {
      type: 'line',
      data: {
        labels: ['Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026'],
        datasets: [{
          label: 'Overall GRC Score',
          data: [61, 65, 70, 75, 79],
          borderColor: '#14B8A6',
          backgroundColor: 'rgba(20,184,166,0.1)',
          borderWidth: 2.5,
          tension: 0.4,
          fill: true,
          pointRadius: 5,
          pointBackgroundColor: '#14B8A6',
        }, {
          label: 'Governance',
          data: [58, 62, 66, 70, 72],
          borderColor: '#F59E0B',
          backgroundColor: 'transparent',
          borderWidth: 1.5,
          tension: 0.4,
          pointRadius: 3,
          borderDash: [4,4],
        }, {
          label: 'Compliance',
          data: [70, 74, 78, 83, 87],
          borderColor: '#22C55E',
          backgroundColor: 'transparent',
          borderWidth: 1.5,
          tension: 0.4,
          pointRadius: 3,
          borderDash: [4,4],
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.04)' } },
          y: {
            min: 40, max: 100,
            grid: { color: 'rgba(255,255,255,0.04)' },
            ticks: { callback: v => v + '%' }
          }
        },
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 10, padding: 10 } },
          tooltip: {
            callbacks: { label: ctx => ` ${ctx.dataset.label}: ${ctx.raw}%` }
          }
        }
      }
    });

    /* ── Gauge (doughnut) ── */
    new Chart(document.getElementById('gaugeChart'), {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [60, 40],
          backgroundColor: [
            'rgba(20,184,166,0.85)',
            'rgba(255,255,255,0.04)',
          ],
          borderWidth: 0,
          circumference: 180,
          rotation: 270,
        }]
      },
      options: {
        responsive: true,
        cutout: '72%',
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });

    /* ── RAG Doughnut ── */
    new Chart(document.getElementById('ragChart'), {
      type: 'doughnut',
      data: {
        labels: ['GREEN', 'AMBER', 'RED'],
        datasets: [{
          data: [12, 4, 1],
          backgroundColor: ['rgba(34,197,94,0.8)', 'rgba(245,158,11,0.8)', 'rgba(239,68,68,0.8)'],
          borderWidth: 0,
          borderRadius: 3,
        }]
      },
      options: {
        responsive: true,
        cutout: '65%',
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw} checks` } }
        }
      }
    });
  }

  function buildKPIs() {
    const kpis = [
      { name: 'Policy Comprehension', val: '78%', target: '≥85%', status: 'amber' },
      { name: 'Training Completion',  val: '91%', target: '≥90%', status: 'green' },
      { name: 'Control Effectiveness',val: '83%', target: '≥80%', status: 'green' },
      { name: 'Open Audit Findings',  val: '2',   target: '≤5',   status: 'green' },
      { name: 'Risk Register Age',    val: '62d', target: '≤90d', status: 'green' },
      { name: 'Open Risk Items',      val: '12',  target: '≤15',  status: 'green' },
      { name: 'Critical Risk Items',  val: '2',   target: '≤1',   status: 'amber' },
      { name: 'FCA Changes Tracked',  val: '100%',target: '100%', status: 'green' },
      { name: 'GRC Platform',         val: 'No',  target: 'Yes',  status: 'red'   },
      { name: 'Board GRC Oversight',  val: 'Yes', target: 'Yes',  status: 'green' },
    ];

    const grid = document.getElementById('kpi-grid');
    kpis.forEach(k => {
      const el = document.createElement('div');
      el.className = 'kpi-row';
      el.innerHTML = `
        <span class="kpi-dot ${k.status}"></span>
        <span class="kpi-name">${k.name}</span>
        <span class="kpi-val">${k.val}</span>
        <span class="kpi-target">/ ${k.target}</span>
      `;
      grid.appendChild(el);
    });
  }
