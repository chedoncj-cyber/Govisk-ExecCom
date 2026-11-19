'use strict';

// ── Region configuration ──────────────────────────────────────────────────────
const REGIONS = {
  'uk': {
    flag: '🇬🇧',
    name: 'United Kingdom',
    accent: '#1d6bb5',
    accentDim: 'rgba(29,107,181,0.12)',
    regulators: 'FCA · CASS · SM&CR · Bank of England · PRA · CBEST · OFSI · FRC',
    countries: 'United Kingdom',
    apiUrl: '/api/fca-updates',
    briefingRegion: 'UK',
    isUK: true,
  },
  'north-america': {
    flag: '🌎',
    name: 'North America',
    accent: '#1a6b3c',
    accentDim: 'rgba(26,107,60,0.12)',
    regulators: 'Fed · SEC · OCC · FDIC · CFTC · FinCEN · OFAC · OSFI · OSC · AMF · FINTRAC',
    countries: 'USA · Canada',
    apiUrl: '/api/regional-updates/north-america',
    briefingRegion: 'North America',
  },
  'latin-america': {
    flag: '🌎',
    name: 'Latin America',
    accent: '#8b6914',
    accentDim: 'rgba(139,105,20,0.12)',
    regulators: 'BCB · CVM · BANXICO · CNBV · SFC · CMF · SBS · BCRA · CNV · GAFILAT',
    countries: 'Brazil · Mexico · Colombia · Chile · Peru · Argentina',
    apiUrl: '/api/regional-updates/latin-america',
    briefingRegion: 'Latin America',
  },
  'europe': {
    flag: '🇪🇺',
    name: 'Europe',
    accent: '#1a4fa8',
    accentDim: 'rgba(26,79,168,0.12)',
    regulators: 'ESMA · ECB/SSM · EBA · AMLA · BaFin · AMF · DNB · CONSOB · CNMV · AFM',
    countries: 'EU · Germany · France · Netherlands · Italy · Spain',
    apiUrl: '/api/regional-updates/europe',
    briefingRegion: 'Europe',
  },
  'asia-pacific': {
    flag: '🌏',
    name: 'Asia-Pacific',
    accent: '#0e7490',
    accentDim: 'rgba(14,116,144,0.12)',
    regulators: 'MAS · HKMA · SFC · NFRA · CSRC · PBOC · FSA · RBI · SEBI · ASIC · APRA · AUSTRAC · APG',
    countries: 'Singapore · Hong Kong · China · Japan · India · Australia',
    apiUrl: '/api/regional-updates/asia-pacific',
    briefingRegion: 'Asia',
  },
  'africa': {
    flag: '🌍',
    name: 'Africa',
    accent: '#9a3412',
    accentDim: 'rgba(154,52,18,0.12)',
    regulators: 'PA/SARB · FSCA · CBN · CBK · CMA · GIABA · ESAAMLG · GABAC',
    countries: 'South Africa · Nigeria · Kenya',
    apiUrl: '/api/regional-updates/africa',
    briefingRegion: 'Africa',
  },
};

const REGION_ORDER = ['uk','north-america','latin-america','europe','asia-pacific','africa'];

// ── Static FATF Fallback Data ─────────────────────────────────────────────────
const FATF_STATIC = {
  updated: 'October 2026',
  black_list: [
    {
      country: 'Democratic People\'s Republic of Korea',
      iso: 'KP', flag: '🇰🇵',
      listed_since: 'February 2011',
      risk_level: 'CRITICAL',
      reason: 'Failure to address significant AML/CFT deficiencies. Presents an ongoing money laundering and terrorism financing risk. UNSC sanctions apply. No bilateral engagement with FATF.'
    },
    {
      country: 'Iran',
      iso: 'IR', flag: '🇮🇷',
      listed_since: 'June 2016',
      risk_level: 'CRITICAL',
      reason: 'Persistent failure to implement FATF recommendations and address terrorism financing risks. Extensive UNSC/OFAC/OFSI sanctions regime. Transactions with Iranian entities present severe regulatory exposure.'
    },
    {
      country: 'Myanmar',
      iso: 'MM', flag: '🇲🇲',
      listed_since: 'February 2023',
      risk_level: 'HIGH',
      reason: 'Significant AML/CFT deficiencies identified following military takeover. Failure to progress FATF action plan. Increased monitoring for drug trafficking proceeds and cross-border illicit finance flows.'
    },
  ],
  grey_list: [
    { country: 'Algeria',              flag: '🇩🇿' },
    { country: 'Angola',               flag: '🇦🇴' },
    { country: 'Burkina Faso',         flag: '🇧🇫' },
    { country: 'Cameroon',             flag: '🇨🇲' },
    { country: 'Côte d\'Ivoire',       flag: '🇨🇮' },
    { country: 'DR Congo',             flag: '🇨🇩' },
    { country: 'Haiti',                flag: '🇭🇹' },
    { country: 'Kenya',                flag: '🇰🇪' },
    { country: 'Laos',                 flag: '🇱🇦' },
    { country: 'Lebanon',              flag: '🇱🇧' },
    { country: 'Mali',                 flag: '🇲🇱' },
    { country: 'Monaco',               flag: '🇲🇨' },
    { country: 'Mozambique',           flag: '🇲🇿' },
    { country: 'Nigeria',              flag: '🇳🇬' },
    { country: 'Philippines',          flag: '🇵🇭' },
    { country: 'Senegal',              flag: '🇸🇳' },
    { country: 'South Sudan',          flag: '🇸🇸' },
    { country: 'Syria',                flag: '🇸🇾' },
    { country: 'Tanzania',             flag: '🇹🇿' },
    { country: 'Vietnam',              flag: '🇻🇳' },
    { country: 'Yemen',                flag: '🇾🇪' },
  ],
};

// ── State ─────────────────────────────────────────────────────────────────────
let _charts = {};
let _reportState = { generated: false };
const _regionFeedState = {};

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const dateEl = document.getElementById('wr-date-input');
  const today = new Date();
  dateEl.value = today.toISOString().slice(0, 10);
  document.getElementById('ticker-date').textContent =
    today.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  Chart.defaults.color = '#94A3B8';
  Chart.defaults.font.family = "'IBM Plex Sans', -apple-system, system-ui, sans-serif";
  Chart.defaults.font.size = 11;
});

// ── Helper: format date ───────────────────────────────────────────────────────
function _fmtDate(d) {
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' });
}

// ── Helper: escape HTML ───────────────────────────────────────────────────────
function _esc(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Helper: animated counter ──────────────────────────────────────────────────
function _animateCount(el, target, suffix = '') {
  if (!el) return;
  const dur = 900;
  const start = performance.now();
  const from  = parseInt(el.textContent) || 0;
  const step  = (now) => {
    const t = Math.min((now - start) / dur, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(from + (target - from) * ease) + suffix;
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// ── Helper: destroy chart ─────────────────────────────────────────────────────
function _destroyChart(id) {
  if (_charts[id]) { _charts[id].destroy(); delete _charts[id]; }
}

// ── Loading steps ─────────────────────────────────────────────────────────────
const STEPS = [
  'Connecting to intelligence feeds…',
  'Fetching FATF blacklist data…',
  'Loading regional MI feeds…',
  'Retrieving enforcement actions…',
  'Pulling daily intelligence briefing…',
  'Compiling world intelligence…',
  'Building charts and analytics…',
  'Finalising report…',
];
let _stepIdx = 0;
let _stepTimer = null;

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

// ── Main: generate report ─────────────────────────────────────────────────────
async function generateReport() {
  const dateVal   = document.getElementById('wr-date-input').value;
  const regionVal = document.getElementById('wr-region-select').value;
  const btn       = document.getElementById('wr-generate-btn');

  if (!dateVal) { _toast('Please select a report date.', 'amber'); return; }

  // Show loading
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
    // Parallel fetch all needed data
    const [fatfData, briefingData, ...regionResults] = await Promise.allSettled([
      _fetchFATF(),
      _fetchBriefing(),
      ...regions.map(r => _fetchRegionData(r)),
    ]);

    const fatf     = fatfData.status === 'fulfilled' ? fatfData.value : FATF_STATIC;
    const briefing = briefingData.status === 'fulfilled' ? briefingData.value : null;
    const regionData = {};
    regions.forEach((r, i) => {
      regionData[r] = regionResults[i].status === 'fulfilled' ? regionResults[i].value : null;
    });

    // Parallel fetch enforcement for all regions
    const enfResults = await Promise.allSettled(regions.map(r => _fetchEnforcement(r)));
    const enfData = {};
    regions.forEach((r, i) => {
      enfData[r] = enfResults[i].status === 'fulfilled' ? enfResults[i].value : null;
    });

    _stopLoadingSteps();
    _renderReport(dateVal, regionVal, regions, fatf, briefing, regionData, enfData);

  } catch (err) {
    _stopLoadingSteps();
    _renderReport(dateVal, regionVal, regions, FATF_STATIC, null, {}, {});
  } finally {
    btn.disabled = false;
    document.getElementById('wr-loading').classList.remove('active');
  }
}

// ── API Fetchers ──────────────────────────────────────────────────────────────
async function _fetchFATF() {
  const r = await fetch('/api/fatf-blacklist');
  if (!r.ok) throw new Error('FATF offline');
  return r.json();
}

async function _fetchBriefing() {
  const r = await fetch('/api/daily-briefing');
  if (!r.ok) throw new Error('Briefing offline');
  return r.json();
}

async function _fetchRegionData(slug) {
  const cfg = REGIONS[slug];
  const r = await fetch(cfg.apiUrl);
  if (!r.ok) throw new Error(`Region ${slug} offline`);
  const data = await r.json();
  return { slug, news: data.news || data[cfg.newsKey] || [], sourced_date: data.sourced_date || '' };
}

async function _fetchEnforcement(slug) {
  const r = await fetch(`/api/enforcement/region/${slug}`);
  if (!r.ok) throw new Error(`Enforcement ${slug} offline`);
  return r.json();
}

// ── Render Report ─────────────────────────────────────────────────────────────
function _renderReport(dateVal, regionVal, regions, fatf, briefing, regionData, enfData) {

  // Compute global stats
  let totalIntel = 0, totalHigh = 0, totalEnf = 0;
  regions.forEach(r => {
    const d = regionData[r];
    if (d && d.news) {
      totalIntel += d.news.length;
      totalHigh  += d.news.filter(n => n.severity === 'RED').length;
    }
    const e = enfData[r];
    if (e && e.cases) totalEnf += e.cases.length;
  });
  const totalFATF = (fatf.black_list || []).length + (fatf.grey_list || []).length;

  // Header
  document.getElementById('wr-meta-date').textContent      = _fmtDate(dateVal);
  document.getElementById('wr-meta-scope').textContent     = regionVal === 'all' ? 'All Regions (Global)' : REGIONS[regions[0]]?.name || regionVal;
  document.getElementById('wr-meta-generated').textContent = new Date().toLocaleString('en-GB', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });

  // Exec stats
  _animateCount(document.getElementById('wr-stat-total'),   totalIntel);
  _animateCount(document.getElementById('wr-stat-high'),    totalHigh);
  _animateCount(document.getElementById('wr-stat-enf'),     totalEnf);
  _animateCount(document.getElementById('wr-stat-fatf'),    totalFATF);
  _animateCount(document.getElementById('wr-stat-regions'), regions.length);

  // Show report
  document.getElementById('wr-report').style.display = 'block';
  document.getElementById('wr-report').classList.add('active');
  document.getElementById('wr-export-pdf-btn').style.display  = 'flex';
  document.getElementById('wr-export-word-btn').style.display = 'flex';

  // Charts
  _buildCharts(regions, regionData, enfData, fatf);

  // FATF
  _renderFATF(fatf);

  // Regions
  _renderAllRegions(regions, regionData, enfData, briefing);

  // Update ticker
  _updateTicker(regions, regionData, enfData);

  // Badge
  document.getElementById('wr-chart1-badge').textContent =
    totalHigh > 0 ? `${totalHigh} HIGH RISK` : 'ALL CLEAR';

  _reportState.generated = true;
  setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
}

// ── Charts ────────────────────────────────────────────────────────────────────
function _buildCharts(regions, regionData, enfData, fatf) {
  // Collect per-region stats
  const rLabels = regions.map(r => REGIONS[r]?.name || r);
  const rHigh   = regions.map(r => regionData[r]?.news?.filter(n => n.severity === 'RED').length    || 0);
  const rMed    = regions.map(r => regionData[r]?.news?.filter(n => n.severity === 'AMBER').length  || 0);
  const rLow    = regions.map(r => regionData[r]?.news?.filter(n => n.severity === 'GREEN').length  || 0);
  const rTotal  = regions.map(r => regionData[r]?.news?.length || 0);
  const rEnf    = regions.map(r => enfData[r]?.cases?.length || 0);

  const totHigh = rHigh.reduce((a,b) => a+b, 0);
  const totMed  = rMed.reduce((a,b) => a+b, 0);
  const totLow  = rLow.reduce((a,b) => a+b, 0);

  // 1. Global Risk Doughnut
  _destroyChart('risk-dist');
  _charts['risk-dist'] = new Chart(document.getElementById('wr-chart-risk-dist'), {
    type: 'doughnut',
    data: {
      labels: ['High Risk', 'Medium Risk', 'Low Risk'],
      datasets: [{
        data: [totHigh, totMed, totLow],
        backgroundColor: ['rgba(239,68,68,0.85)', 'rgba(245,158,11,0.85)', 'rgba(34,197,94,0.75)'],
        borderColor:     ['rgba(239,68,68,0.3)',   'rgba(245,158,11,0.3)',  'rgba(34,197,94,0.3)'],
        borderWidth: 1,
        borderRadius: 3,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      cutout: '60%',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw} items` } },
      },
    },
  });
  // Legend
  const legend = document.getElementById('wr-risk-legend');
  if (legend) {
    legend.innerHTML = [
      { label: 'High Risk',   val: totHigh, c: '#EF4444' },
      { label: 'Medium Risk', val: totMed,  c: '#F59E0B' },
      { label: 'Low Risk',    val: totLow,  c: '#22C55E' },
    ].map(l => `<div style="display:flex;align-items:center;gap:6px;">
      <span style="width:9px;height:9px;border-radius:50%;background:${l.c};flex-shrink:0;"></span>
      <span style="color:var(--text-2)">${l.label}</span>
      <strong style="color:${l.c}">${l.val}</strong>
    </div>`).join('');
  }

  // 2. Regional Bar Chart (stacked)
  _destroyChart('region-bar');
  _charts['region-bar'] = new Chart(document.getElementById('wr-chart-region-bar'), {
    type: 'bar',
    data: {
      labels: rLabels,
      datasets: [
        { label: 'High Risk',   data: rHigh, backgroundColor: 'rgba(239,68,68,0.75)',  borderRadius: 3 },
        { label: 'Medium Risk', data: rMed,  backgroundColor: 'rgba(245,158,11,0.75)', borderRadius: 3 },
        { label: 'Low Risk',    data: rLow,  backgroundColor: 'rgba(34,197,94,0.65)',  borderRadius: 3 },
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

  // 3. Enforcement Bar
  _destroyChart('enf-bar');
  _charts['enf-bar'] = new Chart(document.getElementById('wr-chart-enf-bar'), {
    type: 'bar',
    data: {
      labels: rLabels,
      datasets: [{
        label: 'Enforcement Actions',
        data: rEnf,
        backgroundColor: regions.map(r => `${REGIONS[r]?.accent || '#14B8A6'}CC`),
        borderColor:     regions.map(r => REGIONS[r]?.accent || '#14B8A6'),
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { font: { size: 10 } } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, beginAtZero: true, ticks: { stepSize: 1 } },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` ${ctx.raw} enforcement case${ctx.raw !== 1 ? 's' : ''}` } },
      },
    },
  });

  // 4. FATF Doughnut
  _destroyChart('fatf');
  const blackN = (fatf.black_list || []).length;
  const greyN  = (fatf.grey_list  || []).length;
  _charts['fatf'] = new Chart(document.getElementById('wr-chart-fatf'), {
    type: 'doughnut',
    data: {
      labels: ['Black List', 'Grey List', 'Compliant'],
      datasets: [{
        data: [blackN, greyN, 195 - blackN - greyN],
        backgroundColor: ['rgba(239,68,68,0.85)','rgba(245,158,11,0.75)','rgba(20,184,166,0.5)'],
        borderColor:     ['rgba(239,68,68,0.3)',  'rgba(245,158,11,0.3)', 'rgba(20,184,166,0.2)'],
        borderWidth: 1, borderRadius: 3,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      cutout: '58%',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw} jurisdictions` } },
      },
    },
  });
  const fatfLeg = document.getElementById('wr-fatf-legend');
  if (fatfLeg) {
    fatfLeg.innerHTML = [
      { label: `Black List (${blackN})`, c: '#EF4444' },
      { label: `Grey List (${greyN})`,   c: '#F59E0B' },
      { label: `Compliant (${195 - blackN - greyN})`, c: '#14B8A6' },
    ].map(l => `<div style="display:flex;align-items:center;gap:7px;">
      <span style="width:8px;height:8px;border-radius:50%;background:${l.c};flex-shrink:0;"></span>
      <span style="font-size:0.65rem;color:var(--text-2)">${l.label}</span>
    </div>`).join('');
  }

  // 5. Radar (risk ratio per region)
  _destroyChart('radar');
  const rRatio = rTotal.map((t, i) => t ? Math.round((rHigh[i] / t) * 100) : 0);
  _charts['radar'] = new Chart(document.getElementById('wr-chart-radar'), {
    type: 'radar',
    data: {
      labels: rLabels,
      datasets: [{
        label: 'High Risk %',
        data: rRatio,
        backgroundColor: 'rgba(239,68,68,0.15)',
        borderColor: '#EF4444',
        borderWidth: 2,
        pointBackgroundColor: '#EF4444',
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
        tooltip: { callbacks: { label: ctx => ` High Risk: ${ctx.raw}%` } },
      },
    },
  });
}

// ── Render FATF ───────────────────────────────────────────────────────────────
function _renderFATF(fatf) {
  const blackList = fatf.black_list || FATF_STATIC.black_list;
  const greyList  = fatf.grey_list  || FATF_STATIC.grey_list;
  const updated   = fatf.updated    || fatf.sourced_date || FATF_STATIC.updated;

  document.getElementById('wr-fatf-updated').textContent = updated;
  document.getElementById('wr-fatf-badge').textContent =
    `${blackList.length} BLACK · ${greyList.length} GREY`;
  document.getElementById('wr-fatf-black-count').textContent = `${blackList.length} countries`;
  document.getElementById('wr-fatf-grey-count').textContent  = `${greyList.length} countries`;

  // Black list
  const blackEl = document.getElementById('wr-fatf-black-list');
  blackEl.innerHTML = blackList.map(c => `
    <div class="wr-fatf-country">
      <div class="wr-fatf-flag">${_esc(c.flag || '🏴')}</div>
      <div class="wr-fatf-country-info">
        <div class="wr-fatf-country-name">${_esc(c.country)}</div>
        <div class="wr-fatf-country-since">Listed since ${_esc(c.listed_since || c.since || '—')}</div>
        <div class="wr-fatf-country-reason">${_esc(c.reason || c.detail || '')}</div>
      </div>
      <span style="font-size:0.6rem;font-weight:700;padding:2px 8px;border-radius:4px;background:var(--red-dim);color:var(--red);font-family:'IBM Plex Mono',monospace;flex-shrink:0;align-self:flex-start">${_esc(c.risk_level || 'HIGH')}</span>
    </div>`).join('');

  // Grey list
  const greyEl = document.getElementById('wr-fatf-grey-list');
  greyEl.innerHTML = greyList.map(c => `
    <div class="wr-fatf-grey-item">
      <span class="flag">${_esc(c.flag || '🏳')}</span>
      <span class="name" title="${_esc(c.country)}">${_esc(c.country)}</span>
    </div>`).join('');
}

// ── Render All Regions ────────────────────────────────────────────────────────
function _renderAllRegions(regions, regionData, enfData, briefing) {
  const container = document.getElementById('wr-regions-container');
  container.innerHTML = '';

  regions.forEach(slug => {
    const cfg  = REGIONS[slug];
    const data = regionData[slug];
    const enf  = enfData[slug];
    const news = data?.news || [];

    const el = document.createElement('div');
    el.className = 'wr-region-block';
    el.id = `wr-region-${slug}`;

    el.innerHTML = `
      <!-- Region Section Header -->
      <div class="wr-section-header">
        <div class="wr-section-label">${_esc(cfg.flag)} ${_esc(cfg.name)}</div>
        <div class="wr-section-line"></div>
        <span style="font-size:0.6rem;font-weight:700;padding:2px 10px;border-radius:4px;border:1px solid;font-family:'IBM Plex Mono',monospace;white-space:nowrap;color:${cfg.accent};border-color:${cfg.accent};background:${cfg.accentDim}">${_esc(cfg.countries)}</span>
      </div>

      <!-- Region Hero -->
      <div class="wr-region-hero" style="--region-accent:${cfg.accent};--region-accent-dim:${cfg.accentDim}">
        <div class="wr-region-flag">${_esc(cfg.flag)}</div>
        <div class="wr-region-body">
          <div class="wr-region-kicker">Regional Intelligence</div>
          <div class="wr-region-name">${_esc(cfg.name)}</div>
          <div class="wr-region-regulators">${_esc(cfg.regulators)}</div>
        </div>
        <div class="wr-region-tags">
          <span class="wr-region-tag" style="color:${cfg.accent};border-color:${cfg.accent};background:${cfg.accentDim}">MI Dashboard</span>
          ${data?.sourced_date ? `<span style="font-size:0.6rem;color:var(--text-3);font-family:'IBM Plex Mono',monospace">${_esc(data.sourced_date)}</span>` : ''}
        </div>
      </div>

      <!-- MI Stats -->
      ${_buildMIStats(slug, news)}

      <!-- Risk Distribution -->
      ${_buildRiskBar(news)}

      <!-- Active Regulators -->
      ${_buildRegulatorCloud(slug, news)}

      <!-- Intel Feed -->
      <div style="margin-bottom:14px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:8px;">
          <div style="font-size:0.75rem;font-weight:700;color:var(--text-1)">Reference Intelligence Feed</div>
          <div class="wr-feed-filter" id="wr-filter-${slug}">
            <button class="wr-filter-btn active" data-sev="ALL" onclick="filterFeed('${slug}','ALL',this)">All</button>
            <button class="wr-filter-btn" data-sev="RED" onclick="filterFeed('${slug}','RED',this)">High Risk</button>
            <button class="wr-filter-btn" data-sev="AMBER" onclick="filterFeed('${slug}','AMBER',this)">Medium</button>
            <button class="wr-filter-btn" data-sev="GREEN" onclick="filterFeed('${slug}','GREEN',this)">Low Risk</button>
          </div>
        </div>
        <div class="wr-feed" id="wr-feed-${slug}">${_buildFeedItems(news, 'ALL')}</div>
      </div>

      <!-- Enforcement -->
      ${_buildEnforcement(slug, enf, cfg)}

      <!-- Daily Intelligence -->
      ${_buildBriefing(slug, briefing, cfg)}
    `;

    container.appendChild(el);
    _regionFeedState[slug] = { news, activeSev: 'ALL' };
  });
}

// ── MI Stats ──────────────────────────────────────────────────────────────────
function _buildMIStats(slug, news) {
  const high   = news.filter(n => n.severity === 'RED').length;
  const medium = news.filter(n => n.severity === 'AMBER').length;
  const low    = news.filter(n => n.severity === 'GREEN').length;
  const regs   = new Set(news.map(n => n.regulator).filter(Boolean)).size;

  const cards = [
    { val: news.length, label: 'Intel Items',  c: '#3B82F6',  icon: '📊' },
    { val: high,        label: 'High Risk',    c: '#EF4444',  icon: '🔴' },
    { val: medium,      label: 'Medium Risk',  c: '#F59E0B',  icon: '🟡' },
    { val: low,         label: 'Low Risk',     c: '#22C55E',  icon: '🟢' },
    { val: regs || news.length, label: 'Regulators', c: '#14B8A6', icon: '🏛' },
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
  const total  = news.length || 1;
  const high   = news.filter(n => n.severity === 'RED').length;
  const medium = news.filter(n => n.severity === 'AMBER').length;
  const low    = news.filter(n => n.severity === 'GREEN').length;
  const pct    = n => Math.round((n / total) * 100);
  return `<div class="wr-risk-panel">
    <div class="wr-risk-row">
      <span class="wr-risk-lbl" style="color:var(--red)">HIGH</span>
      <div class="wr-risk-track"><div class="wr-risk-fill" style="background:var(--red);width:${pct(high)}%"></div></div>
      <span class="wr-risk-num" style="color:var(--red)">${high}</span>
      <span class="wr-risk-pct">${pct(high)}%</span>
    </div>
    <div class="wr-risk-row">
      <span class="wr-risk-lbl" style="color:var(--amber)">MED</span>
      <div class="wr-risk-track"><div class="wr-risk-fill" style="background:var(--amber);width:${pct(medium)}%"></div></div>
      <span class="wr-risk-num" style="color:var(--amber)">${medium}</span>
      <span class="wr-risk-pct">${pct(medium)}%</span>
    </div>
    <div class="wr-risk-row">
      <span class="wr-risk-lbl" style="color:var(--green)">LOW</span>
      <div class="wr-risk-track"><div class="wr-risk-fill" style="background:var(--green);width:${pct(low)}%"></div></div>
      <span class="wr-risk-num" style="color:var(--green)">${low}</span>
      <span class="wr-risk-pct">${pct(low)}%</span>
    </div>
  </div>`;
}

// ── Regulator Cloud ───────────────────────────────────────────────────────────
function _buildRegulatorCloud(slug, news) {
  const cfg = REGIONS[slug];
  const uniqueRegs = [...new Set(news.map(n => n.regulator).filter(Boolean))];
  const regs = uniqueRegs.length
    ? uniqueRegs
    : (cfg.regulators || '').split(' · ').filter(Boolean).slice(0, 8);
  return `<div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin-bottom:14px;padding:14px 18px;background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg)">
    <span style="font-size:0.6rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-3);font-family:'IBM Plex Mono',monospace;width:100%;margin-bottom:4px">Active Regulators</span>
    ${regs.map(r => `<span style="font-size:0.65rem;font-weight:600;padding:3px 10px;border-radius:12px;border:1px solid ${cfg.accent};color:${cfg.accent};background:${cfg.accentDim};font-family:'IBM Plex Mono',monospace;white-space:nowrap">${_esc(r)}</span>`).join('')}
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
    const ref = n.reference || n.rule_ref || n.ref || (n.type ? `[${n.type}]` : `[${idx + 1}]`);
    const srcUrl = n.url || n.source_url || '';
    const country = n.country ? `<span class="wr-feed-type">${_esc(n.country)}</span>` : '';
    const regBadge = n.regulator ? `<span class="wr-feed-regulator">${_esc(n.regulator)}</span>` : '';
    const tags = (n.tags || []).map(t => `<span class="wr-feed-tag">${_esc(t)}</span>`).join('');
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

// ── Enforcement ───────────────────────────────────────────────────────────────
function _buildEnforcement(slug, enf, cfg) {
  const cases = enf?.cases || [];
  const title = enf?.title || `${cfg.name} — Enforcement Actions`;
  if (!cases.length) {
    return `<div style="margin-bottom:14px">
      <div style="font-size:0.75rem;font-weight:700;color:var(--text-1);margin-bottom:8px">${_esc(title)}</div>
      <div class="wr-callout">No enforcement data available — start the API server to load live data.</div>
    </div>`;
  }
  return `<div style="margin-bottom:20px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:8px;">
      <div style="font-size:0.75rem;font-weight:700;color:var(--text-1)">${_esc(title)}</div>
      <span style="font-size:0.6rem;font-weight:700;padding:2px 9px;border-radius:4px;background:var(--red-dim);color:var(--red);font-family:'IBM Plex Mono',monospace">${cases.length} recent action${cases.length !== 1 ? 's' : ''}</span>
    </div>
    <div class="wr-enf-grid">
      ${cases.map(c => `<div class="wr-enf-card">
        <div class="wr-enf-top">
          <div class="wr-enf-firm">${_esc(c.firm)}</div>
          <div class="wr-enf-fine">${_esc(c.fine)}</div>
        </div>
        <div class="wr-enf-summary">${_esc(c.summary)}</div>
        <div class="wr-enf-footer">
          <span>${_esc(c.date)}</span>
          <span class="wr-enf-regulator">${_esc(c.regulator)}</span>
        </div>
      </div>`).join('')}
    </div>
  </div>`;
}

// ── Daily Briefing ────────────────────────────────────────────────────────────
function _buildBriefing(slug, briefing, cfg) {
  if (!briefing) {
    return `<div style="margin-bottom:20px">
      <div style="font-size:0.75rem;font-weight:700;color:var(--text-1);margin-bottom:8px">Live Daily Intelligence</div>
      <div class="wr-callout info">Run Update on the main portal to generate live daily intelligence. Click Portal in the navigation.</div>
    </div>`;
  }
  const targetRegion = cfg.briefingRegion.toLowerCase();
  const topics = (briefing.topics || []).filter(t => {
    const r = (t.region || '').toLowerCase();
    return r === targetRegion;
  });
  if (!topics.length) {
    return `<div style="margin-bottom:20px">
      <div style="font-size:0.75rem;font-weight:700;color:var(--text-1);margin-bottom:8px">Live Daily Intelligence — ${_esc(cfg.name)}</div>
      <div class="wr-callout info">No live intelligence yet for ${_esc(cfg.name)} — run a daily update to generate.</div>
    </div>`;
  }

  const RISK_CLS = { HIGH: 'HIGH', MEDIUM: 'MEDIUM', LOW: 'LOW' };
  const cards = topics.map(t => {
    const lines = (t.summary || 'No data.').split('\n').filter(l => l.trim()).map(l =>
      l.startsWith('•') || l.startsWith('-') || l.startsWith('*')
        ? `<li>${_esc(l.replace(/^[•\-*]\s*/, ''))}</li>`
        : `<p>${_esc(l)}</p>`
    ).join('');
    const cites = (t.citations || []).slice(0, 4).map((_, i) =>
      `<span class="wr-cite" title="Reference [${i+1}]">[${i+1}]</span>`
    ).join('');
    const actions = t.key_actions?.length
      ? `<ul class="wr-briefing-actions">${t.key_actions.slice(0,3).map(a => `<li>${_esc(a)}</li>`).join('')}</ul>` : '';
    const risk = t.risk_level
      ? `<span class="wr-briefing-risk ${RISK_CLS[t.risk_level] || ''}">${_esc(t.risk_level)}</span>` : '';
    return `<div class="wr-briefing-card">
      <div class="wr-briefing-head">
        <span class="wr-briefing-icon">${_esc(t.icon || '●')}</span>
        <div class="wr-briefing-title-grp">
          <div class="wr-briefing-title">${_esc(t.title)}</div>
          ${risk}
          ${t.compliance_deadline ? `<div style="font-size:0.6rem;color:var(--amber);font-family:'IBM Plex Mono',monospace;margin-top:3px">Deadline: ${_esc(t.compliance_deadline)}</div>` : ''}
          <div class="wr-status-row">
            <span class="wr-status-label">Status</span>
            <span class="wr-status-chip">⏱ ${_esc(t.status || 'Ongoing')}</span>
          </div>
        </div>
        ${cites ? `<div class="wr-citations">${cites}</div>` : ''}
      </div>
      ${actions}
      <div class="wr-briefing-body">${lines || _esc(t.summary || '')}</div>
    </div>`;
  }).join('');

  const ts = briefing.generated_date
    ? `Updated ${_esc(briefing.generated_date)} ${_esc(briefing.generated_time || '')}` : '';

  return `<div style="margin-bottom:20px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:8px;">
      <div style="font-size:0.75rem;font-weight:700;color:var(--text-1)">Live Daily Intelligence — ${_esc(cfg.name)}</div>
      ${ts ? `<span style="font-size:0.65rem;color:var(--text-3);font-family:'IBM Plex Mono',monospace">${ts}</span>` : ''}
    </div>
    <div class="wr-briefing-grid">${cards}</div>
  </div>`;
}

// ── Update Ticker ─────────────────────────────────────────────────────────────
function _updateTicker(regions, regionData, enfData) {
  const tickerEl = document.getElementById('ticker-scroll');
  if (!tickerEl) return;
  const items = [];
  regions.forEach(r => {
    const cfg  = REGIONS[r];
    const news = regionData[r]?.news || [];
    const high = news.filter(n => n.severity === 'RED').length;
    const enf  = enfData[r]?.cases || [];
    if (high > 0) items.push(`<span class="ticker-item t-red">🔴 ${cfg.name}: ${high} HIGH risk signal${high!==1?'s':''}</span>`);
    if (enf.length > 0) items.push(`<span class="ticker-item t-amber">⚡ ${cfg.name}: ${enf.length} enforcement action${enf.length!==1?'s':''} — ${enf[0]?.firm || ''}</span>`);
  });
  items.push('<span class="ticker-item t-teal">🌐 Govisk ExecCom Region World Report — Generated ' +
    new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) + '</span>');
  tickerEl.innerHTML = items.join('');
}

// ── Download Word ─────────────────────────────────────────────────────────────
function downloadWord() {
  if (!_reportState.generated) { _toast('Generate a report first.', 'amber'); return; }

  const dateVal   = document.getElementById('wr-date-input').value;
  const regionVal = document.getElementById('wr-region-select').value;
  const scopeLabel = regionVal === 'all'
    ? 'All Regions'
    : (REGIONS[regionVal]?.name || regionVal);

  // Grab the visible report HTML
  const reportEl = document.getElementById('wr-report');
  if (!reportEl) return;

  // Build a Word-compatible HTML document (application/msword trick)
  // Charts are excluded in the word export (canvas elements won't render)
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
        h1   { font-size: 20pt; color: #0d4a6e; border-bottom: 2pt solid #14B8A6; padding-bottom: 6pt; }
        h2   { font-size: 15pt; color: #0d4a6e; margin-top: 16pt; border-bottom: 1pt solid #cbd5e1; padding-bottom: 4pt; }
        h3   { font-size: 13pt; color: #1a4fa8; margin-top: 12pt; }
        table { border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 10pt; }
        th   { background: #0d4a6e; color: white; padding: 6pt 8pt; text-align: left; }
        td   { border: 1pt solid #cbd5e1; padding: 5pt 8pt; vertical-align: top; }
        tr:nth-child(even) td { background: #f1f5f9; }
        .kicker { font-size: 8pt; font-weight: bold; color: #14B8A6; letter-spacing: 1pt; text-transform: uppercase; }
        .meta   { font-size: 9pt; color: #64748b; margin-bottom: 4pt; }
        .badge-red    { background: #fee2e2; color: #991b1b; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-amber  { background: #fef3c7; color: #92400e; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-green  { background: #dcfce7; color: #166534; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-blue   { background: #dbeafe; color: #1e40af; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-teal   { background: #ccfbf1; color: #0f766e; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .badge-purple { background: #ede9fe; color: #5b21b6; padding: 1pt 5pt; font-size: 8pt; font-weight: bold; }
        .section-rule { border: none; border-top: 1pt solid #e2e8f0; margin: 12pt 0; }
        .confidential { font-size: 8pt; color: #94a3b8; border-top: 1pt solid #e2e8f0; margin-top: 20pt; padding-top: 8pt; }
        .fatf-black { background: #fee2e2; border-left: 4pt solid #ef4444; padding: 6pt 10pt; margin-bottom: 6pt; }
        .fatf-grey  { display: inline-block; background: #fef3c7; padding: 2pt 6pt; margin: 2pt; font-size: 9pt; }
        .enf-card   { border-left: 3pt solid #ef4444; padding: 6pt 10pt; margin-bottom: 6pt; background: #fafafa; }
        .enf-fine   { font-size: 14pt; font-weight: bold; color: #ef4444; }
        .intel-item { border-left: 3pt solid #cbd5e1; padding: 5pt 10pt; margin-bottom: 5pt; }
        .intel-item.RED    { border-left-color: #ef4444; background: #fff5f5; }
        .intel-item.AMBER  { border-left-color: #f59e0b; background: #fffbeb; }
        .intel-item.GREEN  { border-left-color: #22c55e; background: #f0fdf4; }
        .ref-tag { font-size: 8pt; color: #2563eb; font-weight: bold; }
      </style>
    </head>
    <body>
      <div class="kicker">CONFIDENTIAL — Govisk ExecCom Intelligence Reports</div>
      <h1>ExecCom Region World Report</h1>
      <div class="meta">
        <strong>Report Date:</strong> ${_fmtDate(dateVal)} &nbsp;|&nbsp;
        <strong>Scope:</strong> ${_escWord(scopeLabel)} &nbsp;|&nbsp;
        <strong>Generated:</strong> ${new Date().toLocaleString('en-GB', {day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'})}
      </div>
      <hr class="section-rule"/>
      ${_buildWordFATF()}
      ${_buildWordRegions()}
      <div class="confidential">
        CONFIDENTIAL — For authorised use only. Prepared by Govisk ExecCom Intelligence Reports.
        This report does not constitute legal or regulatory advice.
        Verify material findings at source regulators before action.
        &copy; ${new Date().getFullYear()} Govisk ExecCom Intelligence.
      </div>
    </body>
    </html>`;

  const blob = new Blob(['﻿' + wordHtml], {
    type: 'application/msword; charset=utf-8'
  });
  const url  = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const datePart = dateVal.replace(/-/g, '');
  const regionPart = regionVal === 'all' ? 'World' : (REGIONS[regionVal]?.name || regionVal).replace(/\s+/g, '_');
  link.href     = url;
  link.download = `Govisk_ExecCom_World_Report_${regionPart}_${datePart}.doc`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  _toast('Word document downloaded.', 'green');
}

function _escWord(s) {
  return String(s ?? '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

function _buildWordFATF() {
  const fatf = FATF_STATIC;
  const blackList = fatf.black_list || [];
  const greyList  = fatf.grey_list  || [];
  return `
    <h2>🚨 FATF Blacklist &amp; Grey List</h2>
    <p class="meta">Source: FATF — fatf-gafi.org · ${_escWord(fatf.updated || 'October 2026')}</p>
    <h3>High-Risk Jurisdictions — Call to Action (Black List)</h3>
    ${blackList.map(c => `
      <div class="fatf-black">
        <strong>${_escWord(c.flag || '')} ${_escWord(c.country)}</strong>
        <span class="badge-red">BLACK LIST</span>
        <div class="meta">Listed since: ${_escWord(c.listed_since || '—')}</div>
        <div>${_escWord(c.reason || '')}</div>
      </div>`).join('')}
    <h3>Increased Monitoring — Grey List (${greyList.length} Jurisdictions)</h3>
    <div>${greyList.map(c => `<span class="fatf-grey">${_escWord(c.flag || '')} ${_escWord(c.country)}</span>`).join('')}</div>
    <hr class="section-rule"/>`;
}

function _buildWordRegions() {
  const regionVal = document.getElementById('wr-region-select').value;
  const regions   = regionVal === 'all' ? REGION_ORDER : [regionVal];
  const container = document.getElementById('wr-regions-container');
  if (!container) return '';

  let html = '';
  regions.forEach(slug => {
    const cfg  = REGIONS[slug];
    // Extract intel feed items
    const feedEl = document.getElementById(`wr-feed-${slug}`);
    const feedItems = feedEl ? Array.from(feedEl.querySelectorAll('.wr-feed-item')) : [];

    // Extract enforcement cards
    const enfCards = Array.from(document.querySelectorAll(`#wr-region-${slug} .wr-enf-card`));

    html += `<h2>${_escWord(cfg.flag)} ${_escWord(cfg.name)}</h2>
    <p class="meta">Regulators: ${_escWord(cfg.regulators)}</p>`;

    // Intel feed as table
    if (feedItems.length) {
      html += `<h3>Reference Intelligence Feed (${feedItems.length} items)</h3>
      <table>
        <tr><th>Severity</th><th>Date</th><th>Regulator</th><th>Headline</th><th>Reference</th></tr>
        ${feedItems.map(el => {
          const sev = el.classList.contains('sev-RED') ? 'HIGH' : el.classList.contains('sev-AMBER') ? 'MEDIUM' : 'LOW';
          const date = el.querySelector('.wr-feed-date')?.textContent || '';
          const reg  = el.querySelector('.wr-feed-regulator')?.textContent || '';
          const hl   = el.querySelector('.wr-feed-headline')?.textContent || '';
          const refEl = el.querySelector('.wr-feed-ref');
          const ref  = (refEl?.textContent || '').replace(/\s*↗\s*$/, '');
          const refHref = refEl?.getAttribute('href') || '';
          const cls  = sev === 'HIGH' ? 'badge-red' : sev === 'MEDIUM' ? 'badge-amber' : 'badge-green';
          const refCell = refHref
            ? `<a href="${_escWord(refHref)}" style="color:#2563eb;text-decoration:underline">${_escWord(ref)}</a>`
            : _escWord(ref);
          return `<tr>
            <td><span class="${cls}">${_escWord(sev)}</span></td>
            <td>${_escWord(date)}</td>
            <td>${_escWord(reg)}</td>
            <td>${_escWord(hl)}</td>
            <td class="ref-tag">${refCell}</td>
          </tr>`;
        }).join('')}
      </table>`;
    } else {
      html += '<p class="meta"><em>No intelligence data available — start the API server.</em></p>';
    }

    // Enforcement
    if (enfCards.length) {
      html += `<h3>Enforcement Actions</h3>`;
      enfCards.forEach(card => {
        const firm    = card.querySelector('.wr-enf-firm')?.textContent    || '';
        const fine    = card.querySelector('.wr-enf-fine')?.textContent    || '';
        const summary = card.querySelector('.wr-enf-summary')?.textContent || '';
        const date    = card.querySelector('.wr-enf-footer span:first-child')?.textContent || '';
        const reg     = card.querySelector('.wr-enf-regulator')?.textContent || '';
        html += `<div class="enf-card">
          <strong>${_escWord(firm)}</strong>
          <div class="enf-fine">${_escWord(fine)}</div>
          <div>${_escWord(summary)}</div>
          <div class="meta">${_escWord(date)} · ${_escWord(reg)}</div>
        </div>`;
      });
    }
    html += '<hr class="section-rule"/>';
  });
  return html;
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function _toast(msg, type = 'info') {
  const stack = document.getElementById('toast-stack');
  if (!stack) return;
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.textContent = msg;
  stack.appendChild(el);
  setTimeout(() => el.classList.add('toast-visible'), 50);
  setTimeout(() => { el.classList.remove('toast-visible'); setTimeout(() => el.remove(), 400); }, 4000);
}