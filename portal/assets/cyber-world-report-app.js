'use strict';

// ── Cyber Region Configuration ────────────────────────────────────────────────
const CYBER_REGIONS = {
  'uk': {
    flag: '🇬🇧',
    name: 'United Kingdom',
    accent: '#06B6D4',
    accentDim: 'rgba(6,182,212,0.12)',
    countries: 'United Kingdom',
    apiUrl: '/api/cyber-updates/uk',
  },
  'north-america': {
    flag: '🌎',
    name: 'North America',
    accent: '#3B82F6',
    accentDim: 'rgba(59,130,246,0.12)',
    countries: 'USA · Canada',
    apiUrl: '/api/cyber-updates/north-america',
  },
  'latin-america': {
    flag: '🌎',
    name: 'Latin America',
    accent: '#F59E0B',
    accentDim: 'rgba(245,158,11,0.12)',
    countries: 'Brazil · Mexico · Colombia · Chile · Peru',
    apiUrl: '/api/cyber-updates/latin-america',
  },
  'europe': {
    flag: '🇪🇺',
    name: 'Europe',
    accent: '#8B5CF6',
    accentDim: 'rgba(139,92,246,0.12)',
    countries: 'EU · Germany · France · Netherlands · Spain',
    apiUrl: '/api/cyber-updates/europe',
  },
  'asia-pacific': {
    flag: '🌏',
    name: 'Asia-Pacific',
    accent: '#14B8A6',
    accentDim: 'rgba(20,184,166,0.12)',
    countries: 'Singapore · Japan · India · Australia · China',
    apiUrl: '/api/cyber-updates/asia-pacific',
  },
  'africa': {
    flag: '🌍',
    name: 'Africa',
    accent: '#EF4444',
    accentDim: 'rgba(239,68,68,0.12)',
    countries: 'South Africa · Nigeria · Kenya',
    apiUrl: '/api/cyber-updates/africa',
  },
};

const REGION_ORDER = ['uk','north-america','latin-america','europe','asia-pacific','africa'];

// ── State ─────────────────────────────────────────────────────────────────────
let _charts = {};
let _reportState = { generated: false };
const _regionFeedState = {};

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const dateEl = document.getElementById('wr-date-input');
  const today  = new Date();
  dateEl.value = today.toISOString().slice(0, 10);
  document.getElementById('ticker-date').textContent =
    today.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  Chart.defaults.color = '#94A3B8';
  Chart.defaults.font.family = "'IBM Plex Sans', -apple-system, system-ui, sans-serif";
  Chart.defaults.font.size = 11;
});

// ── Helpers ───────────────────────────────────────────────────────────────────
function _fmtDate(d) {
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' });
}
function _esc(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function _animateCount(el, target, suffix = '') {
  if (!el) return;
  const dur = 900, start = performance.now(), from = parseInt(el.textContent) || 0;
  const step = (now) => {
    const t = Math.min((now - start) / dur, 1), ease = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(from + (target - from) * ease) + suffix;
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}
function _destroyChart(id) {
  if (_charts[id]) { _charts[id].destroy(); delete _charts[id]; }
}

// ── Loading Steps ─────────────────────────────────────────────────────────────
const STEPS = [
  'Connecting to cyber intelligence feeds…',
  'Querying NCSC advisories…',
  'Loading CISA KEV catalogue…',
  'Fetching ENISA threat landscape…',
  'Retrieving JPCERT/CC incident data…',
  'Pulling ASD/ACSC cyber reports…',
  'Aggregating Africa cyber intelligence…',
  'Building threat matrix and charts…',
  'Finalising report…',
];
let _stepIdx = 0, _stepTimer = null;

function _startLoadingSteps() {
  _stepIdx = 0;
  const el = document.getElementById('wr-loading-step');
  if (el) el.textContent = STEPS[0];
  _stepTimer = setInterval(() => {
    _stepIdx = (_stepIdx + 1) % STEPS.length;
    if (el) el.textContent = STEPS[_stepIdx];
  }, 900);
}
function _stopLoadingSteps() {
  if (_stepTimer) { clearInterval(_stepTimer); _stepTimer = null; }
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function _toast(msg, type = 'teal') {
  const stack = document.getElementById('toast-stack');
  if (!stack) return;
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.textContent = msg;
  t.style.cssText = `
    padding: 10px 18px; border-radius: 8px; font-size: 0.78rem; font-weight: 600;
    background: var(--surface-2); border: 1px solid var(--border-2);
    color: var(--text-1); box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    animation: fadeInUp 0.2s ease;
  `;
  stack.appendChild(t);
  setTimeout(() => t.remove(), 3200);
}

// ── Main: generate report ─────────────────────────────────────────────────────
async function generateReport() {
  const dateVal   = document.getElementById('wr-date-input').value;
  const regionVal = document.getElementById('wr-region-select').value;
  const btn       = document.getElementById('wr-generate-btn');

  if (!dateVal) { _toast('Please select a report date.', 'amber'); return; }

  btn.disabled = true;
  document.getElementById('wr-empty').style.display    = 'none';
  document.getElementById('wr-report').style.display   = 'none';
  document.getElementById('wr-report').classList.remove('active');
  document.getElementById('wr-loading').classList.add('active');
  document.getElementById('wr-export-pdf-btn').style.display  = 'none';
  document.getElementById('wr-export-word-btn').style.display = 'none';
  _startLoadingSteps();

  const regions = regionVal === 'all' ? REGION_ORDER : [regionVal];

  try {
    const regionResults = await Promise.allSettled(regions.map(r => _fetchCyberData(r)));
    const regionData = {};
    regions.forEach((r, i) => {
      regionData[r] = regionResults[i].status === 'fulfilled' ? regionResults[i].value : null;
    });
    _stopLoadingSteps();
    _renderReport(dateVal, regionVal, regions, regionData);
  } catch (err) {
    _stopLoadingSteps();
    _renderReport(dateVal, regionVal, regions, {});
  } finally {
    btn.disabled = false;
    document.getElementById('wr-loading').classList.remove('active');
  }
}

// ── API Fetch ─────────────────────────────────────────────────────────────────
async function _fetchCyberData(slug) {
  const r = await fetch(`/api/cyber-updates/${slug}`);
  if (!r.ok) throw new Error(`Cyber ${slug} offline`);
  const data = await r.json();
  return {
    slug,
    news:         data.news    || [],
    bodies:       data.bodies  || [],
    meta:         data.meta    || {},
    sourced_date: data.sourced_date || '',
  };
}

// ── Render Report ─────────────────────────────────────────────────────────────
function _renderReport(dateVal, regionVal, regions, regionData) {
  // Compute global stats
  let totalItems = 0, totalCritical = 0, totalRansomware = 0, totalCVE = 0, totalBodies = 0;
  regions.forEach(r => {
    const d = regionData[r];
    if (d && d.news) {
      totalItems      += d.news.length;
      totalCritical   += d.news.filter(n => n.severity === 'RED').length;
      totalRansomware += d.news.filter(n =>
        (n.tags || []).some(t => t.toLowerCase().includes('ransomware')) ||
        (n.headline || '').toLowerCase().includes('ransomware')
      ).length;
      totalCVE += d.news.filter(n =>
        (n.tags || []).some(t => /cve/i.test(t)) ||
        /vulnerab/i.test(n.type || '') ||
        /cve/i.test(n.headline || '')
      ).length;
    }
    if (d && d.bodies) totalBodies += d.bodies.length;
  });

  // Header
  document.getElementById('wr-meta-date').textContent      = _fmtDate(dateVal);
  document.getElementById('wr-meta-scope').textContent     = regionVal === 'all' ? 'All Regions (Global)' : (CYBER_REGIONS[regions[0]]?.name || regionVal);
  document.getElementById('wr-meta-generated').textContent = new Date().toLocaleString('en-GB', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
  document.getElementById('wr-matrix-updated').textContent = dateVal;

  // KPI counters
  _animateCount(document.getElementById('wr-stat-total'),     totalItems);
  _animateCount(document.getElementById('wr-stat-critical'),  totalCritical);
  _animateCount(document.getElementById('wr-stat-ransomware'),totalRansomware);
  _animateCount(document.getElementById('wr-stat-cve'),       totalCVE);
  _animateCount(document.getElementById('wr-stat-bodies'),    totalBodies);

  // Show report
  document.getElementById('wr-report').style.display = 'block';
  document.getElementById('wr-report').classList.add('active');
  document.getElementById('wr-export-pdf-btn').style.display  = 'flex';
  document.getElementById('wr-export-word-btn').style.display = 'flex';

  // Build charts
  _buildCharts(regions, regionData);

  // Active Threat Matrix
  _renderThreatMatrix(regions, regionData);

  // Per-region sections
  _renderAllRegions(regions, regionData);

  // Update ticker
  _updateTicker(regions, regionData);

  // Chart1 badge
  document.getElementById('wr-chart1-badge').textContent =
    totalCritical > 0 ? `${totalCritical} CRITICAL` : 'ALL CLEAR';

  _reportState.generated = true;
  setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
}

// ── Charts ────────────────────────────────────────────────────────────────────
function _buildCharts(regions, regionData) {
  const rLabels  = regions.map(r => CYBER_REGIONS[r]?.name || r);
  const rHigh    = regions.map(r => regionData[r]?.news?.filter(n => n.severity === 'RED').length   || 0);
  const rMed     = regions.map(r => regionData[r]?.news?.filter(n => n.severity === 'AMBER').length || 0);
  const rLow     = regions.map(r => regionData[r]?.news?.filter(n => n.severity === 'GREEN').length || 0);
  const rTotal   = regions.map(r => regionData[r]?.news?.length || 0);
  const rBodies  = regions.map(r => regionData[r]?.bodies?.length || 0);

  // Aggregate type distribution across all regions
  const typeCounts = {};
  regions.forEach(r => {
    (regionData[r]?.news || []).forEach(n => {
      const t = n.type || 'Unknown';
      typeCounts[t] = (typeCounts[t] || 0) + 1;
    });
  });
  const typeLabels = Object.keys(typeCounts);
  const typeVals   = typeLabels.map(k => typeCounts[k]);
  const typeColors = [
    'rgba(239,68,68,0.85)','rgba(245,158,11,0.85)','rgba(34,197,94,0.75)',
    'rgba(59,130,246,0.85)','rgba(139,92,246,0.75)','rgba(6,182,212,0.80)',
    'rgba(249,115,22,0.75)','rgba(20,184,166,0.75)',
  ];

  // Aggregate tag categories
  const tagCounts = {};
  const TOP_TAGS = ['Ransomware','APT','Phishing','Vulnerability','State Actors','Critical Infrastructure','Data Breach','Enforcement'];
  regions.forEach(r => {
    (regionData[r]?.news || []).forEach(n => {
      (n.tags || []).forEach(tag => {
        const matchedTop = TOP_TAGS.find(t => tag.toLowerCase().includes(t.toLowerCase()));
        if (matchedTop) tagCounts[matchedTop] = (tagCounts[matchedTop] || 0) + 1;
      });
    });
  });
  const catLabels = Object.keys(tagCounts).sort((a, b) => tagCounts[b] - tagCounts[a]).slice(0, 7);
  const catVals   = catLabels.map(k => tagCounts[k]);

  // 1. Threat Type Doughnut
  _destroyChart('threat-dist');
  _charts['threat-dist'] = new Chart(document.getElementById('wr-chart-threat-dist'), {
    type: 'doughnut',
    data: {
      labels: typeLabels,
      datasets: [{
        data: typeVals,
        backgroundColor: typeColors.slice(0, typeLabels.length),
        borderColor:     typeColors.slice(0, typeLabels.length).map(c => c.replace('0.85)','0.3)').replace('0.75)','0.3)').replace('0.80)','0.3)')),
        borderWidth: 1, borderRadius: 3,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '60%',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw} items` } },
      },
    },
  });
  const legend = document.getElementById('wr-threat-legend');
  if (legend) {
    legend.innerHTML = typeLabels.map((l, i) =>
      `<div style="display:flex;align-items:center;gap:6px;">
        <span style="width:9px;height:9px;border-radius:50%;background:${typeColors[i] || '#94A3B8'};flex-shrink:0;"></span>
        <span style="color:var(--text-2)">${l}</span>
        <strong style="color:var(--text-1)">${typeVals[i]}</strong>
      </div>`
    ).join('');
  }

  // 2. Severity by Region Stacked Bar
  _destroyChart('sev-bar');
  _charts['sev-bar'] = new Chart(document.getElementById('wr-chart-sev-bar'), {
    type: 'bar',
    data: {
      labels: rLabels,
      datasets: [
        { label: 'Critical', data: rHigh, backgroundColor: 'rgba(239,68,68,0.75)',  borderRadius: 3 },
        { label: 'Elevated', data: rMed,  backgroundColor: 'rgba(245,158,11,0.75)', borderRadius: 3 },
        { label: 'Low',      data: rLow,  backgroundColor: 'rgba(34,197,94,0.65)',  borderRadius: 3 },
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { font: { size: 10 } } },
        y: { stacked: true, grid: { color: 'rgba(255,255,255,0.04)' }, beginAtZero: true },
      },
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 10, padding: 10 } },
        tooltip: { mode: 'index', intersect: false },
      },
    },
  });

  // 3. Top Threat Categories Bar
  _destroyChart('categories');
  _charts['categories'] = new Chart(document.getElementById('wr-chart-categories'), {
    type: 'bar',
    data: {
      labels: catLabels.length ? catLabels : ['No data'],
      datasets: [{
        label: 'Intel Items',
        data: catVals.length ? catVals : [0],
        backgroundColor: 'rgba(6,182,212,0.7)',
        borderColor:     'rgba(6,182,212,1)',
        borderWidth: 1, borderRadius: 4,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, beginAtZero: true, ticks: { stepSize: 1 } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { font: { size: 9 } } },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` ${ctx.raw} intelligence item${ctx.raw !== 1 ? 's' : ''}` } },
      },
    },
  });

  // 4. Body Coverage Doughnut (per region)
  _destroyChart('bodies');
  const bodyColors = regions.map(r => `${CYBER_REGIONS[r]?.accent || '#06B6D4'}CC`);
  _charts['bodies'] = new Chart(document.getElementById('wr-chart-bodies'), {
    type: 'doughnut',
    data: {
      labels: rLabels,
      datasets: [{
        data: rBodies,
        backgroundColor: bodyColors,
        borderColor:     regions.map(r => CYBER_REGIONS[r]?.accent || '#06B6D4'),
        borderWidth: 1, borderRadius: 2,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '55%',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw} bodies` } },
      },
    },
  });
  const bodiesLeg = document.getElementById('wr-bodies-legend');
  if (bodiesLeg) {
    bodiesLeg.innerHTML = rLabels.map((l, i) =>
      `<div style="display:flex;align-items:center;gap:7px;">
        <span style="width:8px;height:8px;border-radius:50%;background:${bodyColors[i] || '#06B6D4'};flex-shrink:0;"></span>
        <span style="font-size:0.65rem;color:var(--text-2)">${l} (${rBodies[i]})</span>
      </div>`
    ).join('');
  }

  // 5. Radar (critical ratio per region)
  _destroyChart('radar');
  const rRatio = rTotal.map((t, i) => t ? Math.round((rHigh[i] / t) * 100) : 0);
  _charts['radar'] = new Chart(document.getElementById('wr-chart-radar'), {
    type: 'radar',
    data: {
      labels: rLabels,
      datasets: [{
        label: 'Critical %',
        data: rRatio,
        backgroundColor: 'rgba(6,182,212,0.15)',
        borderColor: '#06B6D4',
        borderWidth: 2,
        pointBackgroundColor: '#06B6D4',
        pointRadius: 4,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        r: {
          min: 0, max: 100,
          ticks: { stepSize: 25, color: '#475569', font: { size: 9 } },
          grid: { color: 'rgba(255,255,255,0.05)' },
          angleLines: { color: 'rgba(255,255,255,0.05)' },
          pointLabels: { color: '#94A3B8', font: { size: 10 } },
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` Critical: ${ctx.raw}%` } },
      },
    },
  });
}

// ── Active Threat Matrix ──────────────────────────────────────────────────────
function _renderThreatMatrix(regions, regionData) {
  const tbody = document.getElementById('wr-threat-matrix-body');
  if (!tbody) return;

  const allRed = [];
  regions.forEach(r => {
    const cfg  = CYBER_REGIONS[r];
    const news = regionData[r]?.news || [];
    news.filter(n => n.severity === 'RED').forEach(n => {
      allRed.push({ ...n, regionName: cfg.name, regionFlag: cfg.flag, regionAccent: cfg.accent });
    });
  });

  document.getElementById('wr-matrix-badge').textContent =
    allRed.length > 0 ? `${allRed.length} CRITICAL THREAT${allRed.length !== 1 ? 'S' : ''}` : 'NO CRITICAL THREATS';

  if (!allRed.length) {
    tbody.innerHTML = `<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--green);font-family:'IBM Plex Mono',monospace;font-size:0.72rem">✅ No critical threats identified across selected regions</td></tr>`;
    return;
  }

  tbody.innerHTML = allRed.map(n => {
    const srcUrl = n.url || '';
    const refText = srcUrl
      ? `<a href="${_esc(srcUrl)}" target="_blank" rel="noopener noreferrer" style="color:var(--cyan);text-decoration:none;border-bottom:1px dashed var(--cyan);font-size:0.68rem">${_esc(n.regulator || 'Source')} ↗</a>`
      : `<span style="font-size:0.68rem;color:var(--text-3)">${_esc(n.regulator || '—')}</span>`;
    return `<tr>
      <td>
        <span style="font-size:0.95rem">${_esc(n.regionFlag)}</span>
        <span style="font-size:0.65rem;color:${n.regionAccent};font-family:'IBM Plex Mono',monospace;font-weight:600;display:block">${_esc(n.regionName)}</span>
      </td>
      <td style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:var(--text-3)">${_esc(n.date || '—')}</td>
      <td>${refText}</td>
      <td>
        <span style="font-size:0.6rem;font-weight:700;padding:1px 7px;border-radius:4px;background:var(--surface-3);color:var(--text-3);font-family:'IBM Plex Mono',monospace;text-transform:uppercase">${_esc(n.type || '—')}</span>
      </td>
      <td>
        <div class="wr-threat-headline">${_esc(n.headline || '')}</div>
        ${n.tags && n.tags.length ? `<div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:4px">${n.tags.slice(0,3).map(t => `<span class="wr-feed-tag">${_esc(t)}</span>`).join('')}</div>` : ''}
      </td>
      <td>
        <span style="font-size:0.6rem;font-weight:700;padding:2px 8px;border-radius:4px;background:var(--red-dim);color:var(--red);font-family:'IBM Plex Mono',monospace">CRITICAL</span>
      </td>
    </tr>`;
  }).join('');
}

// ── Render All Regions ────────────────────────────────────────────────────────
function _renderAllRegions(regions, regionData) {
  const container = document.getElementById('wr-regions-container');
  container.innerHTML = '';

  regions.forEach(slug => {
    const cfg    = CYBER_REGIONS[slug];
    const data   = regionData[slug];
    const news   = data?.news   || [];
    const bodies = data?.bodies || [];

    const el = document.createElement('div');
    el.className = 'wr-region-block';
    el.id = `wr-region-${slug}`;

    el.innerHTML = `
      <div class="wr-section-header">
        <div class="wr-section-label">${_esc(cfg.flag)} ${_esc(cfg.name)}</div>
        <div class="wr-section-line"></div>
        <span style="font-size:0.6rem;font-weight:700;padding:2px 10px;border-radius:4px;border:1px solid;font-family:'IBM Plex Mono',monospace;white-space:nowrap;color:${cfg.accent};border-color:${cfg.accent};background:${cfg.accentDim}">${_esc(cfg.countries)}</span>
      </div>

      <div class="wr-region-hero" style="--region-accent:${cfg.accent};--region-accent-dim:${cfg.accentDim}">
        <div class="wr-region-flag">${_esc(cfg.flag)}</div>
        <div class="wr-region-body">
          <div class="wr-region-kicker">Cyber Intelligence</div>
          <div class="wr-region-name">${_esc(cfg.name)}</div>
          <div class="wr-region-regulators">${_esc(data?.meta?.bodies || bodies.map(b => b.name).join(' · ') || '—')}</div>
        </div>
        <div class="wr-region-tags">
          <span class="wr-region-tag" style="color:${cfg.accent};border-color:${cfg.accent};background:${cfg.accentDim}">Cyber Feed</span>
          ${data?.sourced_date ? `<span style="font-size:0.6rem;color:var(--text-3);font-family:'IBM Plex Mono',monospace">${_esc(data.sourced_date)}</span>` : ''}
        </div>
      </div>

      ${_buildMIStats(slug, news)}
      ${_buildRiskBar(news)}
      ${_buildBodyBadges(bodies, cfg)}

      <div style="margin-bottom:14px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:8px;">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-1)">Cyber Intelligence Feed</div>
          <div class="wr-feed-filter" id="wr-filter-${slug}">
            <button class="wr-filter-btn active" data-sev="ALL" onclick="filterFeed('${slug}','ALL',this)">All</button>
            <button class="wr-filter-btn" data-sev="RED" onclick="filterFeed('${slug}','RED',this)">Critical</button>
            <button class="wr-filter-btn" data-sev="AMBER" onclick="filterFeed('${slug}','AMBER',this)">Elevated</button>
            <button class="wr-filter-btn" data-sev="GREEN" onclick="filterFeed('${slug}','GREEN',this)">Low</button>
          </div>
        </div>
        <div class="wr-feed" id="wr-feed-${slug}">${_buildFeedItems(news, 'ALL')}</div>
      </div>
    `;

    container.appendChild(el);
    _regionFeedState[slug] = { news, activeSev: 'ALL' };
  });
}

// ── MI Stats ──────────────────────────────────────────────────────────────────
function _buildMIStats(slug, news) {
  const critical = news.filter(n => n.severity === 'RED').length;
  const elevated = news.filter(n => n.severity === 'AMBER').length;
  const low      = news.filter(n => n.severity === 'GREEN').length;
  const sources  = new Set(news.map(n => n.regulator).filter(Boolean)).size;
  const cards = [
    { val: news.length, label: 'Advisories',  c: '#06B6D4', icon: '🛡️' },
    { val: critical,    label: 'Critical',     c: '#EF4444', icon: '🔴' },
    { val: elevated,    label: 'Elevated',     c: '#F59E0B', icon: '🟡' },
    { val: low,         label: 'Low',          c: '#22C55E', icon: '🟢' },
    { val: sources || news.length, label: 'Sources', c: '#3B82F6', icon: '🏛️' },
  ];
  return `<div class="wr-mi-grid">
    ${cards.map(c => `<div class="wr-mi-card" style="--mi-c:${c.c}">
      <span class="wr-mi-icon">${c.icon}</span>
      <div class="wr-mi-value">${c.val}</div>
      <div class="wr-mi-label">${c.label}</div>
    </div>`).join('')}
  </div>`;
}

// ── Risk Bar ──────────────────────────────────────────────────────────────────
function _buildRiskBar(news) {
  const total    = news.length || 1;
  const critical = news.filter(n => n.severity === 'RED').length;
  const elevated = news.filter(n => n.severity === 'AMBER').length;
  const low      = news.filter(n => n.severity === 'GREEN').length;
  const pct      = n => Math.round((n / total) * 100);
  return `<div class="wr-risk-panel">
    <div class="wr-risk-row">
      <span class="wr-risk-lbl" style="color:var(--red)">CRIT</span>
      <div class="wr-risk-track"><div class="wr-risk-fill" style="background:var(--red);width:${pct(critical)}%"></div></div>
      <span class="wr-risk-num" style="color:var(--red)">${critical}</span>
      <span class="wr-risk-pct">${pct(critical)}%</span>
    </div>
    <div class="wr-risk-row">
      <span class="wr-risk-lbl" style="color:var(--amber)">ELEV</span>
      <div class="wr-risk-track"><div class="wr-risk-fill" style="background:var(--amber);width:${pct(elevated)}%"></div></div>
      <span class="wr-risk-num" style="color:var(--amber)">${elevated}</span>
      <span class="wr-risk-pct">${pct(elevated)}%</span>
    </div>
    <div class="wr-risk-row">
      <span class="wr-risk-lbl" style="color:var(--green)">LOW</span>
      <div class="wr-risk-track"><div class="wr-risk-fill" style="background:var(--green);width:${pct(low)}%"></div></div>
      <span class="wr-risk-num" style="color:var(--green)">${low}</span>
      <span class="wr-risk-pct">${pct(low)}%</span>
    </div>
  </div>`;
}

// ── Cyber Body Badges ─────────────────────────────────────────────────────────
function _buildBodyBadges(bodies, cfg) {
  if (!bodies || !bodies.length) return '';
  const extLinkIcon = `<svg width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>`;
  return `<div class="wr-body-grid">
    <span class="wr-body-label">Cyber Bodies Monitored</span>
    ${bodies.map(b => `
      <a class="wr-body-badge" href="${_esc(b.url || '#')}" target="_blank" rel="noopener noreferrer"
         title="${_esc(b.full)}"
         style="color:${cfg.accent};border-color:${cfg.accent};background:${cfg.accentDim}">
        ${_esc(b.name)} ${extLinkIcon}
      </a>`).join('')}
  </div>`;
}

// ── Feed Items ────────────────────────────────────────────────────────────────
function _buildFeedItems(news, filterSev) {
  const items = filterSev && filterSev !== 'ALL'
    ? news.filter(n => n.severity === filterSev)
    : news;

  if (!items.length) {
    return `<div class="wr-callout">No intelligence items for this filter — try All or check API connectivity.</div>`;
  }

  return items.slice(0, 20).map((n, idx) => {
    const ref    = n.reference || n.rule_ref || n.ref || (n.type ? `[${n.type}]` : `[${idx + 1}]`);
    const srcUrl = n.url || n.source_url || '';
    const country  = n.country  ? `<span class="wr-feed-type">${_esc(n.country)}</span>`   : '';
    const regBadge = n.regulator ? `<span class="wr-feed-regulator">${_esc(n.regulator)}</span>` : '';
    const tags   = (n.tags || []).map(t => `<span class="wr-feed-tag">${_esc(t)}</span>`).join('');
    const refBadge = srcUrl
      ? `<a class="wr-feed-ref" href="${_esc(srcUrl)}" target="_blank" rel="noopener noreferrer" title="Source: ${_esc(srcUrl)}">${_esc(ref)} ↗</a>`
      : `<span class="wr-feed-ref" title="Intelligence Reference">${_esc(ref)}</span>`;
    return `<div class="wr-feed-item sev-${n.severity || 'GREEN'}">
      <div class="wr-feed-dot"></div>
      <div class="wr-feed-body">
        <div class="wr-feed-meta">
          <span class="wr-feed-date">${_esc(n.date || '')}</span>
          ${regBadge}${country}
          ${n.type ? `<span class="wr-feed-type">${_esc(n.type)}</span>` : ''}
          ${refBadge}
        </div>
        <div class="wr-feed-headline">${_esc(n.headline || n.title || '')}</div>
        <div class="wr-feed-detail">${_esc(n.detail || n.summary || '')}</div>
        ${tags ? `<div class="wr-feed-tags">${tags}</div>` : ''}
      </div>
    </div>`;
  }).join('');
}

// ── Filter Feed ───────────────────────────────────────────────────────────────
function filterFeed(slug, sev, btn) {
  const state = _regionFeedState[slug];
  if (!state) return;
  document.querySelectorAll(`#wr-filter-${slug} .wr-filter-btn`).forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  state.activeSev = sev;
  const feedEl = document.getElementById(`wr-feed-${slug}`);
  if (feedEl) feedEl.innerHTML = _buildFeedItems(state.news, sev);
}

// ── Update Ticker ─────────────────────────────────────────────────────────────
function _updateTicker(regions, regionData) {
  const tickerEl = document.getElementById('ticker-scroll');
  if (!tickerEl) return;
  const items = [];
  regions.forEach(r => {
    const cfg    = CYBER_REGIONS[r];
    const news   = regionData[r]?.news || [];
    const critical = news.filter(n => n.severity === 'RED').length;
    if (critical > 0) items.push(`<span class="ticker-item t-red">🔴 ${cfg.name}: ${critical} critical threat${critical!==1?'s':''}</span>`);
  });
  items.push('<span class="ticker-item t-teal">🔐 Govisk Cyber Intelligence Report — Generated ' +
    new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) + '</span>');
  tickerEl.innerHTML = items.join('');
}

// ── Word Export ───────────────────────────────────────────────────────────────
function downloadWord() {
  if (!_reportState.generated) { _toast('Generate a report first.', 'amber'); return; }

  const dateVal    = document.getElementById('wr-date-input').value;
  const regionVal  = document.getElementById('wr-region-select').value;
  const scopeLabel = regionVal === 'all'
    ? 'All Regions'
    : (CYBER_REGIONS[regionVal]?.name || regionVal);

  const wordHtml = `
    <!DOCTYPE html>
    <html xmlns:o="urn:schemas-microsoft-com:office:office"
          xmlns:w="urn:schemas-microsoft-com:office:word"
          xmlns="http://www.w3.org/TR/REC-html40">
    <head>
      <meta charset="UTF-8"/>
      <!--[if gte mso 9]>
      <xml><w:WordDocument><w:View>Print</w:View><w:Zoom>90</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml>
      <![endif]-->
      <style>
        body { font-family: Calibri, Arial, sans-serif; font-size: 11pt; color: #1a1a2e; margin: 2cm; }
        h1   { font-size: 20pt; color: #0891b2; border-bottom: 2pt solid #06B6D4; padding-bottom: 6pt; }
        h2   { font-size: 15pt; color: #0891b2; margin-top: 16pt; border-bottom: 1pt solid #cbd5e1; padding-bottom: 4pt; }
        h3   { font-size: 13pt; color: #0e7490; margin-top: 12pt; }
        table { border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 10pt; }
        th   { background: #0891b2; color: white; padding: 6pt 8pt; text-align: left; }
        td   { border: 1pt solid #cbd5e1; padding: 5pt 8pt; vertical-align: top; }
        tr:nth-child(even) td { background: #f0fdfe; }
        .kicker { font-size: 8pt; font-weight: bold; color: #06B6D4; letter-spacing: 1pt; text-transform: uppercase; }
        .meta   { font-size: 9pt; color: #64748b; margin-bottom: 4pt; }
        .badge-red    { background: #fee2e2; color: #991b1b; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-amber  { background: #fef3c7; color: #92400e; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-green  { background: #dcfce7; color: #166534; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-cyan   { background: #cffafe; color: #0e7490; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .section-rule { border: none; border-top: 1pt solid #e2e8f0; margin: 12pt 0; }
        .confidential { font-size: 8pt; color: #94a3b8; border-top: 1pt solid #e2e8f0; margin-top: 20pt; padding-top: 8pt; }
        .threat-row   { border-left: 4pt solid #ef4444; padding: 6pt 10pt; margin-bottom: 6pt; background: #fff5f5; }
        .intel-item   { border-left: 3pt solid #cbd5e1; padding: 5pt 10pt; margin-bottom: 5pt; }
        .intel-item.RED    { border-left-color: #ef4444; background: #fff5f5; }
        .intel-item.AMBER  { border-left-color: #f59e0b; background: #fffbeb; }
        .intel-item.GREEN  { border-left-color: #22c55e; background: #f0fdf4; }
        .ref-tag { font-size: 8pt; color: #2563eb; font-weight: bold; }
        .body-badge { display: inline-block; background: #e0f2fe; color: #0369a1; padding: 2pt 6pt; margin: 2pt; font-size: 9pt; font-weight: bold; }
      </style>
    </head>
    <body>
      <div class="kicker">CONFIDENTIAL — Govisk Cyber Intelligence Reports</div>
      <h1>🔐 Cyber Intelligence World Region Report</h1>
      <div class="meta">
        <strong>Report Date:</strong> ${_fmtDate(dateVal)} &nbsp;|&nbsp;
        <strong>Scope:</strong> ${_escWord(scopeLabel)} &nbsp;|&nbsp;
        <strong>Generated:</strong> ${new Date().toLocaleString('en-GB', {day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'})}
      </div>
      <hr class="section-rule"/>
      ${_buildWordThreatMatrix()}
      ${_buildWordRegions()}
      <div class="confidential">
        CONFIDENTIAL — For authorised use only. Prepared by Govisk ExecCom Intelligence Reports.
        Cyber intelligence sourced from NCSC, CISA, ENISA, JPCERT/CC, ASD/ACSC, ngCERT and regional partners.
        This report does not constitute legal or regulatory advice.
        Verify material findings at source agencies before action.
        &copy; ${new Date().getFullYear()} Govisk ExecCom Intelligence.
      </div>
    </body>
    </html>`;

  const blob = new Blob(['﻿' + wordHtml], { type: 'application/msword; charset=utf-8' });
  const url  = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const datePart   = dateVal.replace(/-/g, '');
  const regionPart = regionVal === 'all' ? 'World' : (CYBER_REGIONS[regionVal]?.name || regionVal).replace(/\s+/g, '_');
  link.href     = url;
  link.download = `Govisk_Cyber_Intelligence_Report_${regionPart}_${datePart}.doc`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  _toast('Cyber Intelligence Word document downloaded.', 'green');
}

function _escWord(s) {
  return String(s ?? '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

function _buildWordThreatMatrix() {
  const matrixBody = document.getElementById('wr-threat-matrix-body');
  if (!matrixBody) return '';
  const rows = Array.from(matrixBody.querySelectorAll('tr'));
  if (!rows.length) return '';

  let html = `<h2>🔴 Active Threat Matrix — Critical Threats</h2>
  <table>
    <thead><tr><th>Region</th><th>Date</th><th>Source</th><th>Type</th><th>Threat Headline</th><th>Severity</th></tr></thead>
    <tbody>`;

  rows.forEach(row => {
    const cells = Array.from(row.querySelectorAll('td'));
    if (cells.length < 5) return;
    const region    = (cells[0]?.textContent || '').trim().replace(/\s+/g, ' ');
    const date      = (cells[1]?.textContent || '').trim();
    const source    = (cells[2]?.textContent || '').trim();
    const type      = (cells[3]?.textContent || '').trim();
    const headline  = (cells[4]?.textContent || '').trim();
    const sevCls    = 'badge-red';
    html += `<tr><td>${_escWord(region)}</td><td>${_escWord(date)}</td><td>${_escWord(source)}</td><td>${_escWord(type)}</td><td>${_escWord(headline)}</td><td><span class="${sevCls}">CRITICAL</span></td></tr>`;
  });

  html += `</tbody></table><hr class="section-rule"/>`;
  return html;
}

function _buildWordRegions() {
  const regionVal = document.getElementById('wr-region-select').value;
  const regions   = regionVal === 'all' ? REGION_ORDER : [regionVal];
  let html = '';

  regions.forEach(slug => {
    const cfg    = CYBER_REGIONS[slug];
    const feedEl = document.getElementById(`wr-feed-${slug}`);
    const feedItems = feedEl ? Array.from(feedEl.querySelectorAll('.wr-feed-item')) : [];

    html += `<h2>${_escWord(cfg.flag)} ${_escWord(cfg.name)} — Cyber Intelligence</h2>
    <p class="meta">Countries: ${_escWord(cfg.countries)}</p>`;

    if (feedItems.length) {
      html += `<h3>Intelligence Feed (${feedItems.length} items)</h3>
      <table><thead><tr><th>Date</th><th>Source</th><th>Type</th><th>Headline</th><th>Detail</th><th>Severity</th><th>Reference</th></tr></thead><tbody>`;

      feedItems.forEach(el => {
        const sev     = el.className.includes('sev-RED') ? 'RED' : el.className.includes('sev-AMBER') ? 'AMBER' : 'GREEN';
        const sevCls  = sev === 'RED' ? 'badge-red' : sev === 'AMBER' ? 'badge-amber' : 'badge-green';
        const date    = el.querySelector('.wr-feed-date')?.textContent?.trim() || '';
        const reg     = el.querySelector('.wr-feed-regulator')?.textContent?.trim() || '';
        const type    = Array.from(el.querySelectorAll('.wr-feed-type')).map(e => e.textContent.trim()).join(', ');
        const headline = el.querySelector('.wr-feed-headline')?.textContent?.trim() || '';
        const detail   = el.querySelector('.wr-feed-detail')?.textContent?.trim() || '';
        const refEl    = el.querySelector('.wr-feed-ref');
        const ref      = (refEl?.textContent || '').replace(/\s*↗\s*$/, '');
        const refHref  = refEl?.getAttribute('href') || '';
        const refCell  = refHref
          ? `<a href="${_escWord(refHref)}" style="color:#2563eb;text-decoration:underline">${_escWord(ref)}</a>`
          : _escWord(ref);

        html += `<tr class="intel-item ${sev}"><td>${_escWord(date)}</td><td>${_escWord(reg)}</td><td>${_escWord(type)}</td><td><strong>${_escWord(headline)}</strong></td><td>${_escWord(detail)}</td><td><span class="${sevCls}">${sev}</span></td><td>${refCell}</td></tr>`;
      });

      html += `</tbody></table>`;
    } else {
      html += `<p class="meta">No intelligence feed items loaded.</p>`;
    }
    html += `<hr class="section-rule"/>`;
  });
  return html;
}