/* ===== CASS Intelligence — Regional MI Page ===== */
'use strict';

// ── Region configuration ──────────────────────────────────────────────────────
const REGION_CONFIG = {
  'uk': {
    flag: '🇬🇧',
    name: 'United Kingdom',
    accent: '#1d6bb5',
    accentDim: 'rgba(29,107,181,0.12)',
    regulators: 'FCA · CASS · SM&CR · Bank of England · PRA · CBEST · OFSI · FRC',
    countries: 'United Kingdom',
    apiUrl: '/api/fca-updates',
    newsKey: 'news',
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
    newsKey: 'news',
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
    newsKey: 'news',
    briefingRegion: 'Latin America',
  },
  'asia-pacific': {
    flag: '🌏',
    name: 'Asia-Pacific',
    accent: '#0e7490',
    accentDim: 'rgba(14,116,144,0.12)',
    regulators: 'MAS · HKMA · SFC · NFRA · CSRC · PBOC · FSA · RBI · SEBI · ASIC · APRA · AUSTRAC · APG',
    countries: 'Singapore · Hong Kong · China · Japan · India · Australia',
    apiUrl: '/api/regional-updates/asia-pacific',
    newsKey: 'news',
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
    newsKey: 'news',
    briefingRegion: 'Africa',
  },
  'europe': {
    flag: '🇪🇺',
    name: 'Europe',
    accent: '#1a4fa8',
    accentDim: 'rgba(26,79,168,0.12)',
    regulators: 'ESMA · ECB/SSM · EBA · AMLA · BaFin · AMF · DNB · CONSOB · CNMV · AFM',
    countries: 'EU · Germany · France · Netherlands · Italy · Spain',
    apiUrl: '/api/regional-updates/europe',
    newsKey: 'news',
    briefingRegion: 'Europe',
  },
};

// ── Slug from URL (/region/uk → 'uk') ─────────────────────────────────────────
const _slug = window.location.pathname.replace(/^\/region\//, '').replace(/\/$/, '');
const _cfg  = REGION_CONFIG[_slug];

if (!_cfg) {
  window.location.replace('/');
  throw new Error('Unknown region');
}

// ── Apply accent theme ────────────────────────────────────────────────────────
document.documentElement.style.setProperty('--rp-accent',     _cfg.accent);
document.documentElement.style.setProperty('--rp-accent-dim', _cfg.accentDim);

// ── Animate counter ───────────────────────────────────────────────────────────
function _animateStat(el, target) {
  if (!el || isNaN(target)) return;
  const dur = 700, step = 16;
  const start = parseInt(el.textContent) || 0;
  let t = 0;
  const tick = () => {
    t += step;
    const p = Math.min(t / dur, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(start + (target - start) * ease);
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

// ── Render hero ───────────────────────────────────────────────────────────────
function renderHero(cfg) {
  const intelligenceLabel = _slug === 'uk' ? 'CASS Intelligence' : 'Regulatory Intelligence';
  document.title = `${cfg.name} — ${intelligenceLabel}`;
  document.getElementById('page-title').textContent = `${cfg.name} — ${intelligenceLabel}`;
  document.getElementById('rp-breadcrumb').textContent = cfg.name;
  document.getElementById('rp-flag').textContent = cfg.flag;
  document.getElementById('rp-title').textContent = cfg.name + ' — Regulatory Intelligence';
  document.getElementById('rp-regulators-subtitle').textContent = cfg.regulators;
  document.getElementById('rp-updated').textContent = cfg.countries;
}

// ── Populate MI stats ─────────────────────────────────────────────────────────
function renderMI(news) {
  const high   = news.filter(n => n.severity === 'RED').length;
  const medium = news.filter(n => n.severity === 'AMBER').length;
  const low    = news.filter(n => n.severity === 'GREEN').length;
  const total  = news.length;
  const regs   = new Set(news.map(n => n.regulator).filter(Boolean)).size;

  _animateStat(document.getElementById('mi-total'),     total);
  _animateStat(document.getElementById('mi-high'),      high);
  _animateStat(document.getElementById('mi-medium'),    medium);
  _animateStat(document.getElementById('mi-low'),       low);
  _animateStat(document.getElementById('mi-regulators'), regs || news.length);

  // Risk bars
  const pct = (n) => total ? Math.round((n / total) * 100) : 0;
  setTimeout(() => {
    document.getElementById('rbar-high').style.width   = pct(high) + '%';
    document.getElementById('rbar-med').style.width    = pct(medium) + '%';
    document.getElementById('rbar-low').style.width    = pct(low) + '%';
    document.getElementById('rbar-high-n').textContent = high;
    document.getElementById('rbar-med-n').textContent  = medium;
    document.getElementById('rbar-low-n').textContent  = low;
    document.getElementById('rbar-high-p').textContent = pct(high) + '%';
    document.getElementById('rbar-med-p').textContent  = pct(medium) + '%';
    document.getElementById('rbar-low-p').textContent  = pct(low) + '%';
  }, 200);

  // Regulator cloud
  const cloud = document.getElementById('rp-reg-cloud');
  const uniqueRegs = [...new Set(news.map(n => n.regulator).filter(Boolean))];
  if (uniqueRegs.length) {
    cloud.innerHTML = `<span class="rp-reg-label">Active Regulators</span>` +
      uniqueRegs.map(r => `<span class="rp-reg-chip">${r}</span>`).join('');
  } else {
    // For UK (FCA news has no regulator field) — show fixed list
    const ukRegs = ['FCA', 'PRA', 'Bank of England', 'CBEST', 'OFSI'];
    cloud.innerHTML = `<span class="rp-reg-label">Active Regulators</span>` +
      ukRegs.map(r => `<span class="rp-reg-chip">${r}</span>`).join('');
  }
}

// ── Render reference feed ─────────────────────────────────────────────────────
let _allNews = [];
let _activeSev = 'ALL';

function renderRefFeed(news, filterSev) {
  const feed = document.getElementById('rp-ref-feed');
  if (!feed) return;
  const items = filterSev && filterSev !== 'ALL'
    ? news.filter(n => n.severity === filterSev)
    : news;
  if (!items.length) {
    feed.innerHTML = '<div class="reg-item"><div class="reg-dot"></div><div class="reg-body"><div class="reg-headline" style="color:var(--text-3)">No items for this filter.</div></div></div>';
    return;
  }
  feed.innerHTML = items.map(n => {
    const country = n.country ? `<span class="reg-country">${n.country}</span>` : '';
    const regBadge = n.regulator ? `<span class="reg-type">${n.regulator}</span>` : '';
    return `
    <div class="reg-item sev-${n.severity}">
      <div class="reg-dot"></div>
      <div class="reg-body">
        <div class="reg-meta">
          <span class="reg-date">${n.date || ''}</span>
          ${regBadge}${country}
          <span class="reg-type">${n.type || ''}</span>
        </div>
        <div class="reg-headline">${n.headline}</div>
        <div class="reg-detail">${n.detail}</div>
        <div class="reg-tags">${(n.tags || []).map(t => `<span class="reg-tag">${t}</span>`).join('')}</div>
      </div>
    </div>`;
  }).join('');
}

// ── Severity filter bar ───────────────────────────────────────────────────────
function initFilterBar() {
  document.getElementById('rp-filter-bar')?.addEventListener('click', e => {
    const btn = e.target.closest('.rp-filter-btn');
    if (!btn) return;
    document.querySelectorAll('.rp-filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    _activeSev = btn.dataset.sev;
    renderRefFeed(_allNews, _activeSev);
  });
}

// ── Render daily briefing cards for this region ───────────────────────────────
function renderBriefing(briefing) {
  const grid = document.getElementById('rp-briefing-grid');
  const ts   = document.getElementById('rp-briefing-ts');
  if (!grid) return;

  if (ts && briefing.generated_date) {
    ts.textContent = `Updated ${briefing.generated_date} ${briefing.generated_time || ''}`;
  }

  const topics = (briefing.topics || []).filter(t => {
    const r = (t.region || '').toLowerCase();
    const target = _cfg.briefingRegion.toLowerCase();
    return r === target;
  });

  if (!topics.length) {
    grid.innerHTML = '<div class="briefing-empty">No live intelligence available for this region yet — click <strong>Run Update</strong> on the main portal to generate.</div>';
    return;
  }

  const RISK_CLS = { HIGH: 'risk-high', MEDIUM: 'risk-medium', LOW: 'risk-low' };

  grid.innerHTML = topics.map(t => {
    const hasError = t.error && t.error !== 'no_scan';
    const provBadge = t.provider ? `<span class="briefing-provider">${t.provider}</span>` : '';
    const enrichBadge = t.enriched_by ? `<span class="briefing-provider enriched">+ ${t.enriched_by}</span>` : '';
    const riskBadge = t.risk_level ? `<span class="risk-badge ${RISK_CLS[t.risk_level] || ''}">${t.risk_level}</span>` : '';
    const deadline = t.compliance_deadline ? `<span class="briefing-deadline"><span class="briefing-deadline-label">Deadline</span> ${t.compliance_deadline}</span>` : '';
    const cites = (t.citations || []).slice(0, 3).map((_, i) => `<span class="briefing-citation">[${i+1}]</span>`).join('');

    const insightHtml = t.insight
      ? `<div class="briefing-insight">${t.insight}</div>` : '';
    const actionsHtml = t.key_actions?.length
      ? `<ul class="briefing-actions">${t.key_actions.map(a => `<li>${a}</li>`).join('')}</ul>` : '';

    const summary = t.summary || 'No data.';
    const lines = summary.split('\n').filter(l => l.trim()).map(l =>
      l.startsWith('•') || l.startsWith('-') || l.startsWith('*')
        ? `<li>${l.replace(/^[•\-*]\s*/, '')}</li>`
        : `<p>${l}</p>`
    ).join('');

    return `<div class="briefing-card${hasError ? ' briefing-card--error' : ''}">
      <div class="briefing-card-head">
        <span class="briefing-icon">${t.icon || '●'}</span>
        <div class="briefing-title-group">
          <span class="briefing-card-title">${t.title}</span>
          ${riskBadge ? `<div class="briefing-risk-row">${riskBadge}</div>` : ''}
          ${deadline ? `<div class="briefing-deadline-row">${deadline}</div>` : ''}
          <div class="briefing-status-row"><span class="briefing-status-label">Status</span><span class="briefing-status-chip">⏱ ${t.status || 'Ongoing'}</span></div>
        </div>
        <span class="briefing-card-meta">${cites}</span>
      </div>
      ${insightHtml}${actionsHtml}
      <div class="briefing-card-body${t.insight ? ' briefing-card-body--secondary' : ''}">${lines || summary}</div>
    </div>`;
  }).join('');
}

// ── Report Suite ─────────────────────────────────────────────────────────────
const REPORT_SUITE = [
  { id: 'cass_health_check',        icon: '📊', title: 'CASS Health Check',           tag: 'CASS 6 & 7', desc: 'Reconciliation gaps, pool compliance, CASS 7.13.4R RAG scoring.' },
  { id: 'cass_resolution_pack',     icon: '📋', title: 'CASS Resolution Pack',        tag: 'CASS 10',    desc: 'Client asset return readiness, 48-hour retrieval test.' },
  { id: 'client_money_segregation', icon: '🔒', title: 'Client Money Segregation',    tag: 'CASS 7',     desc: 'Segregation method, CMA reconciliation, daily compliance.' },
  { id: 'cass_breach_log',          icon: '⚠️', title: 'CASS Breach Log',            tag: 'BREACH',     desc: 'Breach documentation, root cause, regulator notification status.' },
  { id: 'cass_oversight',           icon: '👁', title: 'CASS Oversight (COOF)',       tag: 'COOF',       desc: 'Board reporting, oversight function compliance.' },
  { id: 'threat_intelligence',      icon: '🎯', title: 'Threat Intelligence',         tag: 'INTEL',      desc: 'Sector threat landscape, fraud typologies, insider risk.' },
  { id: 'cyber_threat_assessment',  icon: '🛡', title: 'Cyber Threat Assessment',     tag: 'CYBER',      desc: 'Pen test status, MFA, endpoint protection, CBEST/DORA scoring.' },
  { id: 'fca_incident_response',    icon: '🔔', title: 'Incident Response',           tag: '24HR',       desc: '24-hour operational incident reporting, breach procedures.' },
  { id: 'due_diligence',            icon: '🔍', title: 'Due Diligence',               tag: 'DD',         desc: 'Fit & Proper checks, third-party compliance, sanctions screening.' },
  { id: 'country_risk',             icon: '🌐', title: 'Country Risk',                tag: 'RISK',       desc: 'Sanctions, FATF status, AML risk rating, local custody.' },
  { id: 'executive_protection',     icon: '👤', title: 'Executive Protection',        tag: 'SM&CR',      desc: 'Senior Manager risk briefings, SM&CR mapping, travel risk.' },
  { id: 'physical_security_audit',  icon: '🏢', title: 'Physical Security Audit',     tag: 'PHYSICAL',   desc: 'Access control, CCTV, alarms, operational resilience.' },
  { id: 'grc_report',               icon: '📈', title: 'GRC Intelligence Report',     tag: 'GRC',        desc: 'Governance, Risk & Compliance maturity — OCEG/COSO methodology.' },
];

// ── Regional body overrides for the 4 CASS-specific reports ──────────────────
const _REGIONAL_REPORTS = {
  cass_health_check: {
    uk:             { title: 'CASS Health Check',                        tag: 'CASS 6 & 7', desc: 'Reconciliation gaps, pool compliance, CASS 7.13.4R RAG scoring. FCA CP26/37 SM&CR Phase 2 · CASS 15 safeguarding.' },
    'north-america':{ title: 'SEC / BSA-AML Client Assets Health Check', tag: 'SEC / CFTC', desc: 'SEC Rule 15c3-3 customer protection, BSA/AML compliance. BofA $1.21B & AmEx $350M enforcement context · DeFi startup registration rules.' },
    'asia-pacific': { title: 'MAS / ASIC / HKMA Client Protection Check',tag: 'MAS / ASIC', desc: 'FAA/SFA safeguarding, ASIC AFSL client money segregation, HKMA anti-bribery. Sir Money Changer revocation & ASIC A$4.356M context · MAS Digital Token Advisor for startups.' },
    africa:         { title: 'FSCA / CBN / CBK Client Funds Health Check',tag: 'FSCA / CBN', desc: 'FAIS Act client fund protection, CBN AML compliance. Banxso R2.8bn deepfake AI enforcement context · CBK BNPL startup rules & open banking.' },
    'latin-america':{ title: 'BCB / CVM Client Funds Health Check',      tag: 'BCB / CVM',  desc: 'BCB payment system compliance, CVM client asset protection. VASP enforcement & Ano Bom fraud context · Nubank/fintech open finance compliance.' },
    europe:         { title: 'MiCA / DORA Client Assets Health Check',   tag: 'MiCA / DORA',desc: 'MiCA CASP client asset segregation, DORA operational resilience. BaFin Wirecard €18.3M enforcement · AMLA fintech priorities & 61% DORA non-compliance benchmark.' },
  },
  cass_resolution_pack: {
    uk:             { title: 'CASS Resolution Pack Readiness',           tag: 'CASS 10',    desc: 'Client asset return readiness, 48-hour retrieval test. CASS 10.2.2R compliance.' },
    'north-america':{ title: 'SEC / SIPC Asset Return Readiness',        tag: 'SEC / SIPC', desc: 'SEC customer protection resolution, SIPC asset return plan. 48-hour retrieval planning aligned to post-BofA $1.21B & AmEx $350M enforcement standards.' },
    'asia-pacific': { title: 'MAS / ASIC Asset Resolution Readiness',    tag: 'MAS / ASIC', desc: 'MAS FAA resolution planning, ASIC AFCA client asset recovery. 48-hour retrieval readiness post Sir Money Changer revocation & ASIC enforcement.' },
    africa:         { title: 'FSCA / CBN Recovery Plan Readiness',       tag: 'FSCA / CBN', desc: 'FSCA FSR Act recovery plans, CBN client fund retrieval readiness. Post-Banxso R2.8bn enforcement · CBK BNPL resolution requirements.' },
    'latin-america':{ title: 'BCB / CVM Resolution Readiness',           tag: 'BCB / CVM',  desc: 'BCB payment resolution, CVM client asset recovery planning. VASP resolution requirements post-BCB enforcement · FATF grey list compliance.' },
    europe:         { title: 'DORA / MiFID II Recovery Plan Readiness',  tag: 'DORA',       desc: 'DORA operational recovery plans, MiFID II client asset resolution. 61% non-compliance benchmark · BaFin & ESMA enforcement context.' },
  },
  cass_breach_log: {
    uk:             { title: 'CASS Breach Log & Remediation',            tag: 'CASS BREACH',desc: 'Breach documentation, root cause, FCA notification status. John Wood Group £12.9M & Patrick Dawkins ban · FCA CP26/37 SM&CR Phase 2.' },
    'north-america':{ title: 'SEC / FINRA Violation Log',                tag: 'SEC / FINRA',desc: 'SEC 17a-11 / FINRA Rule 4530 violation reporting. BofA $1.21B & AmEx $350M enforcement · SEC fraud charges & DeFi startup registration breach log.' },
    'asia-pacific': { title: 'MAS / ASIC / SEBI Breach Register',        tag: 'MAS / ASIC', desc: 'MAS incident reporting, ASIC breach register, SEBI call recording obligations. Sir Money Changer revocation & HKMA anti-bribery breach context · Digital Token Advisor compliance.' },
    africa:         { title: 'FSCA / CBN / CBK Violation Register',      tag: 'FSCA / CBN', desc: 'FSCA FAIS breach log, CBN AML violation register. Banxso AI deepfake R2.8bn enforcement · CBN data localisation breaches & CBK BNPL startup violations.' },
    'latin-america':{ title: 'BCB / CVM Breach Log',                     tag: 'BCB / CVM',  desc: 'BCB payment breach log, CVM violation register. VASP enforcement & Ano Bom fraud documentation · FATF grey list breach tracking for fintech operators.' },
    europe:         { title: 'DORA / MiCA Incident Register',            tag: 'DORA / MiCA',desc: 'DORA operational incident log, MiCA CASP breach register. BaFin Wirecard €18.3M enforcement · AMLA fintech breach priorities & ESMA/EBA reporting obligations.' },
  },
  cass_oversight: {
    uk:             { title: 'CASS Oversight (COOF)',                    tag: 'COOF',       desc: 'Board reporting, oversight function compliance. COOF individual accountability under SM&CR · FCA CP26/37 SM&CR Phase 2 — PS19/26 mortgage cap.' },
    'north-america':{ title: 'CCO / BSA Compliance Oversight Report',    tag: 'CCO / BSA',  desc: 'Chief Compliance Officer oversight, SEC/BSA board compliance reporting. Post-BofA $1.21B & AmEx $350M enforcement · DeFi startup CCO governance requirements.' },
    'asia-pacific': { title: 'MAS / ASIC Board Compliance Oversight',    tag: 'MAS / ASIC', desc: 'MAS/ASIC board oversight, HKMA anti-bribery governance. Sir Money Changer AML oversight failure · SEBI call recording board responsibilities & Digital Token Advisor oversight.' },
    africa:         { title: 'FSCA / CBN Board Compliance Report',       tag: 'FSCA / CBN', desc: 'FSCA oversight, CBN board governance compliance. Post-Banxso AI fraud oversight failure · CBK BNPL & open banking board supervision requirements.' },
    'latin-america':{ title: 'BCB / CVM Governance & Oversight',         tag: 'BCB / CVM',  desc: 'BCB governance oversight, CVM board compliance reporting. VASP oversight obligations · Nubank/fintech open finance board governance & FATF compliance supervision.' },
    europe:         { title: 'ESMA / AMLA Governance Oversight',         tag: 'ESMA / AMLA',desc: 'ESMA/EBA board oversight, AMLA fintech governance priorities. DORA 61% non-compliance oversight · BaFin Wirecard post-enforcement governance requirements.' },
  },
};

function injectSuiteStyles() {
  if (document.getElementById('rp-suite-styles')) return;
  const s = document.createElement('style');
  s.id = 'rp-suite-styles';
  s.textContent = `
    .rp-suite-section { margin-top: 32px; }
    .rp-suite-header { margin-bottom: 16px; }
    .rp-suite-title { font-size: 1.05rem; font-weight: 700; color: var(--text-1); letter-spacing: -0.02em; margin-bottom: 4px; }
    .rp-suite-sub { font-size: 0.72rem; color: var(--text-3); font-family: 'IBM Plex Mono', monospace; }
    .rp-suite-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 10px; }
    .rp-suite-card {
      display: flex; align-items: flex-start; gap: 12px;
      padding: 14px 16px; border-radius: 10px;
      background: var(--surface-1); border: 1px solid var(--border-dim);
      text-decoration: none; color: inherit;
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    .rp-suite-card:hover { border-color: var(--rp-accent); box-shadow: 0 0 0 2px var(--rp-accent-dim); }
    .rp-suite-icon { font-size: 1.3rem; line-height: 1; flex-shrink: 0; margin-top: 1px; }
    .rp-suite-body { flex: 1; min-width: 0; }
    .rp-suite-tag {
      display: inline-block; font-size: 0.58rem; font-weight: 700;
      letter-spacing: 0.09em; text-transform: uppercase; padding: 2px 7px;
      border-radius: 10px; border: 1px solid var(--rp-accent);
      color: var(--rp-accent); background: var(--rp-accent-dim);
      font-family: 'IBM Plex Mono', monospace; margin-bottom: 4px;
    }
    .rp-suite-name { font-size: 0.82rem; font-weight: 700; color: var(--text-1); margin-bottom: 2px; }
    .rp-suite-desc { font-size: 0.70rem; color: var(--text-3); line-height: 1.45; }
    .rp-suite-arrow { font-size: 0.85rem; color: var(--text-3); flex-shrink: 0; margin-top: 3px; transition: color 0.15s; }
    .rp-suite-card:hover .rp-suite-arrow { color: var(--rp-accent); }
  `;
  document.head.appendChild(s);
}

function renderReportSuite() {
  const section = document.getElementById('rp-report-suite');
  if (!section) return;
  injectSuiteStyles();
  section.innerHTML = `
    <div class="rp-suite-header">
      <div class="rp-suite-title">Report Suite — ${_cfg.name}</div>
      <div class="rp-suite-sub">Generate all 13 intelligence reports scoped to ${_cfg.name} regulatory frameworks · click any card to open the portal</div>
    </div>
    <div class="rp-suite-grid">
      ${REPORT_SUITE.map(r => {
        const ov    = _REGIONAL_REPORTS[r.id] && _REGIONAL_REPORTS[r.id][_slug];
        const title = ov ? ov.title : r.title;
        const tag   = ov ? ov.tag   : r.tag;
        const desc  = ov ? ov.desc  : r.desc;
        return `<a class="rp-suite-card" href="/portal?region=${_slug}&report=${r.id}">
          <span class="rp-suite-icon">${r.icon}</span>
          <div class="rp-suite-body">
            <span class="rp-suite-tag">${tag}</span>
            <div class="rp-suite-name">${title}</div>
            <div class="rp-suite-desc">${desc}</div>
          </div>
          <span class="rp-suite-arrow">→</span>
        </a>`;
      }).join('')}
    </div>`;
}

// ── Main boot ─────────────────────────────────────────────────────────────────
async function init() {
  renderHero(_cfg);
  initFilterBar();

  // Set ref feed subtitle
  const sub = document.getElementById('rp-feed-subtitle');
  if (sub) sub.textContent = _cfg.regulators;
  const refTitle = document.getElementById('rp-ref-title');
  if (refTitle) refTitle.textContent = `${_cfg.name} — Reference Intelligence`;

  // Parallel data fetch
  const [newsRes, briefingRes] = await Promise.allSettled([
    fetch(_cfg.apiUrl),
    fetch('/api/daily-briefing'),
  ]);

  // Reference news
  if (newsRes.status === 'fulfilled' && newsRes.value.ok) {
    try {
      const data   = await newsRes.value.json();
      const news   = data[_cfg.newsKey] || data.news || [];
      _allNews = news;

      // Updated date from sourced_date or most recent item
      const updated = data.sourced_date || (news[0] && news[0].date) || '';
      if (updated) document.getElementById('rp-updated').textContent = `${_cfg.countries} · ${updated}`;

      renderMI(news);
      renderRefFeed(news, 'ALL');
    } catch { /* render will stay at loading placeholder */ }
  } else {
    document.getElementById('rp-ref-feed').innerHTML =
      '<div class="reg-item"><div class="reg-dot"></div><div class="reg-body"><div class="reg-headline" style="color:var(--text-3)">Intelligence offline — start the API server</div></div></div>';
  }

  // Daily briefing
  if (briefingRes.status === 'fulfilled' && briefingRes.value.ok) {
    try {
      const briefing = await briefingRes.value.json();
      renderBriefing(briefing);
    } catch {
      document.getElementById('rp-briefing-grid').innerHTML =
        '<div class="briefing-empty">No live briefing available.</div>';
    }
  } else {
    document.getElementById('rp-briefing-grid').innerHTML =
      '<div class="briefing-empty">Run Update on the main portal to generate live intelligence.</div>';
  }

  renderReportSuite();
  await renderEnforcement();
  initTickerDate();
}

function initTickerDate() {
  const el = document.getElementById('ticker-date');
  if (el) el.textContent = new Date().toLocaleDateString('en-GB', {day:'2-digit',month:'short',year:'numeric'});
}

async function renderEnforcement() {
  const section = document.getElementById('enf-section');
  const titleEl = document.getElementById('enf-section-title');
  const badgeEl = document.getElementById('enf-badge');
  const cardsEl = document.getElementById('enf-cards');
  if (!section || !cardsEl) return;

  try {
    const resp = await fetch(`/api/enforcement/region/${_slug}`);
    if (!resp.ok) { section.style.display = 'none'; return; }
    const data = await resp.json();

    if (titleEl) titleEl.textContent = data.title || 'Enforcement Actions';
    const cases = data.cases || [];
    if (badgeEl) badgeEl.textContent = `${cases.length} recent action${cases.length !== 1 ? 's' : ''}`;

    if (!cases.length) {
      cardsEl.innerHTML = '<div style="color:var(--text-3);font-size:0.78rem;padding:20px 0;font-family:\'IBM Plex Mono\',monospace">No enforcement data available for this region.</div>';
      return;
    }

    cardsEl.innerHTML = cases.map(c => `
      <div class="enf-card">
        <div class="enf-card-top">
          <div class="enf-firm">${_esc(c.firm)}</div>
          <div class="enf-fine">${_esc(c.fine)}</div>
        </div>
        <div class="enf-summary">${_esc(c.summary)}</div>
        <div class="enf-footer">
          <span class="enf-date">${_esc(c.date)}</span>
          <span class="enf-regulator">${_esc(c.regulator)}</span>
        </div>
      </div>`).join('');

    // Populate region ticker with enforcement highlights
    const tickerEl = document.getElementById('ticker-scroll');
    if (tickerEl) {
      const cfg = _cfg || {};
      const items = [
        ...(cases.slice(0, 3).map(c => `<span class="ticker-item t-red">${_esc(c.regulator)} · ${_esc(c.firm)} — ${_esc(c.fine)} fine · ${_esc(c.date)}</span>`)),
        `<span class="ticker-item t-amber">${cfg.name || _slug.toUpperCase()} Regional Intelligence — ${cfg.regulators || ''}</span>`,
      ];
      tickerEl.innerHTML = items.join('');
    }
  } catch (e) {
    section.style.display = 'none';
  }
}

function _esc(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Scroll fade-in for region pages
const _sfio = new IntersectionObserver(entries => entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); }), {threshold:0.08});
document.querySelectorAll('.fade-in').forEach(el => _sfio.observe(el));

document.addEventListener('DOMContentLoaded', init);
