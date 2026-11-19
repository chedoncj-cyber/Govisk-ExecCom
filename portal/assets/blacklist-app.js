// ── Data & State ──────────────────────────────────────────────────────────────
var _data        = null;
var _activeRegion = 'all';
var REGIONS = ['Africa', 'Americas', 'Asia-Pacific', 'Europe', 'Middle East & North Africa'];

// ── Fetch ─────────────────────────────────────────────────────────────────────
async function loadData() {
  try {
    var res = await fetch('/api/fatf-blacklist');
    if (!res.ok) throw new Error('API returned ' + res.status);
    _data = await res.json();
    render();
    updateStats();
    updateTimestamp();
  } catch (err) {
    document.getElementById('content-area').innerHTML =
      '<div class="empty-state">Failed to load FATF data — ' + err.message + '</div>';
  }
}

async function refreshData() {
  document.getElementById('last-updated').textContent = 'Refreshing…';
  try {
    var res = await fetch('/api/fatf-blacklist/refresh', { method: 'POST' });
    if (res.headers.get('content-type') && res.headers.get('content-type').includes('event-stream')) {
      var reader = res.body.getReader();
      var decoder = new TextDecoder();
      while (true) {
        var chunk = await reader.read();
        if (chunk.done) break;
        var text = decoder.decode(chunk.value);
        var lines = text.split('\n');
        for (var l of lines) {
          if (l.startsWith('data: ')) {
            try {
              var ev = JSON.parse(l.slice(6));
              if (ev.type === 'complete') { await loadData(); return; }
            } catch (e) {}
          }
        }
      }
    }
    await loadData();
  } catch (err) {
    document.getElementById('last-updated').textContent = 'Refresh failed';
  }
}

// ── Stats ─────────────────────────────────────────────────────────────────────
function updateStats() {
  if (!_data || !_data.summary) return;
  document.getElementById('stat-black').textContent = _data.summary.total_black;
  document.getElementById('stat-grey').textContent  = _data.summary.total_grey;
  document.getElementById('stat-total').textContent = _data.summary.total;
}

function updateTimestamp() {
  if (!_data || !_data.last_updated) return;
  var d = new Date(_data.last_updated);
  var method = _data.fetch_method === 'live_scrape' ? 'live' : 'baseline';
  document.getElementById('last-updated').textContent =
    'Updated: ' + d.toLocaleDateString('en-GB', { day:'2-digit', month:'short', year:'numeric' }) +
    ' ' + d.toLocaleTimeString('en-GB', { hour:'2-digit', minute:'2-digit' }) + ' (' + method + ')';
}

// ── Render ────────────────────────────────────────────────────────────────────
function filterList(list) {
  if (_activeRegion === 'all') return list;
  return list.filter(function(c) { return c.region === _activeRegion; });
}

function countryCard(c, statusClass) {
  var concerns = '';
  if (c.primary_concerns && c.primary_concerns.length) {
    concerns = '<div class="card-concerns">' +
      c.primary_concerns.map(function(x) { return '<div class="card-concern-item">' + x + '</div>'; }).join('') +
      '</div>';
  }
  var badgeLabel = statusClass === 'black' ? 'BLACKLIST' : 'GREY LIST';
  return '<div class="country-card status-' + statusClass + '">' +
    '<div class="card-flag">' + (c.flag || '&#127760;') + '</div>' +
    '<div class="card-body">' +
      '<div class="card-name">' + c.country + '</div>' +
      '<div class="card-region">' + c.region + '</div>' +
      '<span class="card-status-badge ' + statusClass + '">' + badgeLabel + '</span>' +
      (c.on_list_since ? '<div class="card-since">On list since: ' + c.on_list_since + '</div>' : '') +
      concerns +
    '</div>' +
  '</div>';
}

function sectionHTML(list, statusClass, title) {
  var filtered = filterList(list);
  if (!filtered.length) return '';
  var badgeClass = statusClass === 'black' ? 'black' : 'grey';
  var badgeLabel = statusClass === 'black'
    ? 'HIGH-RISK — CALL FOR ACTION'
    : 'INCREASED MONITORING';
  return '<div class="list-section">' +
    '<div class="list-section-header">' +
      '<span class="section-badge ' + badgeClass + '">' + badgeLabel + '</span>' +
      '<span class="section-title-text">' + title + '</span>' +
      '<span class="section-count">' + filtered.length + ' jurisdiction' + (filtered.length !== 1 ? 's' : '') + '</span>' +
    '</div>' +
    '<div class="country-grid">' +
      filtered.map(function(c) { return countryCard(c, statusClass); }).join('') +
    '</div>' +
  '</div>';
}

function render() {
  if (!_data) return;

  // Rebuild per-region stats in tabs
  updateRegionTabCounts();

  var html = '';

  // Black list section
  html += sectionHTML(_data.black_list, 'black', 'Black List — No active engagement with FATF');

  // If showing a region, check if no entries in either list
  var greyFiltered = filterList(_data.grey_list);
  var blackFiltered = filterList(_data.black_list);
  if (!greyFiltered.length && !blackFiltered.length) {
    html = '<div class="empty-state">No high-risk jurisdictions in this region.</div>';
  } else {
    // Grey list section
    html += sectionHTML(_data.grey_list, 'grey', 'Grey List — Jurisdictions under Increased Monitoring');
  }

  document.getElementById('content-area').innerHTML = html;
}

function updateRegionTabCounts() {
  if (!_data) return;
  REGIONS.forEach(function(region) {
    var blackCount = _data.black_list.filter(function(c) { return c.region === region; }).length;
    var greyCount  = _data.grey_list.filter(function(c) { return c.region === region; }).length;
    var total = blackCount + greyCount;
    var btn = document.querySelector('.tab-btn[data-region="' + region + '"]');
    if (btn && total > 0) {
      var regionShort = region.replace('Middle East & North Africa', 'MENA');
      btn.innerHTML = regionShort + ' <span style="opacity:0.55;font-size:10px">(' + total + ')</span>';
    }
  });
  // All tab
  var allBtn = document.querySelector('.tab-btn[data-region="all"]');
  if (allBtn && _data.summary) {
    allBtn.innerHTML = 'All Regions <span style="opacity:0.55;font-size:10px">(' + _data.summary.total + ')</span>';
  }
}

// ── Tab Handling ──────────────────────────────────────────────────────────────
document.getElementById('tab-bar').addEventListener('click', function(e) {
  var btn = e.target.closest('.tab-btn');
  if (!btn) return;
  document.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  _activeRegion = btn.dataset.region;
  render();
});

// ── Boot ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', loadData);