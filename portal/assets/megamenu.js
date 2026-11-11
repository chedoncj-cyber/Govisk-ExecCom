/* Govisk ExecCom — Mega Menu  v1.0 */
(function () {
  'use strict';

  var CHEVRON = '<svg class="mm-chevron" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">'
    + '<path d="M2 4.5l4 4 4-4" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
    + '</svg>';

  /* ── Menu data ─────────────────────────────────────────────── */
  var MENU = [
    {
      label: 'Intelligence',
      type: 'mega',
      activePaths: ['/region'],
      columns: [
        {
          head: 'Regional MI Feeds',
          items: [
            { icon: '🇬🇧', title: 'United Kingdom',  desc: 'FCA · CASS · SM&CR · PRA',       href: '/region/uk' },
            { icon: '🇪🇺', title: 'Europe',           desc: 'ESMA · EBA · BaFin · AMLA',       href: '/region/europe' },
            { icon: '🌎', title: 'North America',     desc: 'SEC · FinCEN · OCC · OSFI',       href: '/region/north-america' },
            { icon: '🌎', title: 'Latin America',     desc: 'BCB · CVM · CNBV · GAFILAT',      href: '/region/latin-america' },
            { icon: '🌏', title: 'Asia-Pacific',      desc: 'MAS · ASIC · HKMA · FSA',         href: '/region/asia-pacific' },
            { icon: '🌍', title: 'Africa',            desc: 'FSCA · CBN · CBK · CMA',          href: '/region/africa' }
          ]
        },
        {
          head: 'Live Intelligence',
          items: [
            { icon: '⚡', title: 'ExecCom Portal',    desc: 'Real-time regulatory dashboard',  href: '/portal',        featured: true },
            { icon: '🔴', title: 'FATF Blacklist',    desc: 'Live black & grey list monitor',  href: '/blacklist',     alert: true },
            { icon: '📊', title: 'GRC Dashboard',     desc: 'Governance risk & compliance',    href: '/grc_dashboard' }
          ]
        }
      ],
      footer: [
        { label: 'Open Portal →', href: '/portal',       style: 'primary' },
        { label: 'Request Demo',  href: '/request-demo', style: 'ghost' }
      ]
    },
    {
      label: 'Reports',
      type: 'mega',
      activePaths: ['/portal'],
      columns: [
        {
          head: 'CASS Suite',
          items: [
            { icon: '📊', title: 'Health Check',       desc: 'CASS 6 & 7 reconciliation scoring', href: '/portal?report=cass_health_check' },
            { icon: '📋', title: 'Resolution Pack',    desc: 'CASS 10 — 48h retrieval readiness',  href: '/portal?report=cass_resolution_pack' },
            { icon: '🔒', title: 'Client Money',       desc: 'CASS 7 daily reconciliation audit',  href: '/portal?report=client_money_segregation' },
            { icon: '⚠️',  title: 'Breach Log',         desc: 'Breach documentation & remediation', href: '/portal?report=cass_breach_log' },
            { icon: '👁',  title: 'COOF Oversight',    desc: 'Board reporting & compliance',       href: '/portal?report=cass_oversight' }
          ]
        },
        {
          head: 'Security & Risk',
          items: [
            { icon: '🎯', title: 'Threat Intel',         desc: 'Fraud, insider risk, sanctions',   href: '/portal?report=threat_intelligence' },
            { icon: '🛡',  title: 'Cyber Assessment',    desc: 'CBEST, PS21/3, DORA scoring',      href: '/portal?report=cyber_threat_assessment' },
            { icon: '🔔', title: 'Incident Response',    desc: 'FCA 24h breach notification',      href: '/portal?report=fca_incident_response' },
            { icon: '🔍', title: 'Due Diligence',        desc: 'Fit & Proper, third-party CASS',   href: '/portal?report=due_diligence' },
            { icon: '🌐', title: 'Country Risk',         desc: 'Sanctions, FATF, AML rating',      href: '/portal?report=country_risk' },
            { icon: '👤', title: 'Executive Protection', desc: 'SM&CR mapping & travel risk',      href: '/portal?report=executive_protection' },
            { icon: '📈', title: 'GRC Report',           desc: 'OCEG / COSO maturity assessment',  href: '/portal?report=grc_report' }
          ]
        }
      ],
      footer: [
        { label: 'All Reports →',  href: '/portal',       style: 'primary' },
        { label: 'GRC Templates',  href: '/grc-templates', style: 'ghost' }
      ]
    },
    {
      label: 'Compliance',
      type: 'dropdown',
      activePaths: ['/blacklist', '/grc-templates', '/grc_dashboard'],
      items: [
        { icon: '🔴', title: 'FATF Blacklist',   href: '/blacklist' },
        { icon: '📄', title: 'GRC Templates',    href: '/grc-templates' },
        { icon: '📊', title: 'GRC Dashboard',    href: '/grc_dashboard' }
      ]
    },
    {
      label: 'Company',
      type: 'dropdown',
      activePaths: ['/about', '/services', '/case-studies', '/contact'],
      items: [
        { icon: '🏢', title: 'About Us',      href: '/about' },
        { icon: '⚙️',  title: 'Services',      href: '/services' },
        { icon: '📁', title: 'Case Studies',  href: '/case-studies' },
        { icon: '✉️',  title: 'Contact Us',    href: '/contact' }
      ]
    }
  ];

  /* ── DOM helpers ───────────────────────────────────────────── */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  /* ── Active path check ─────────────────────────────────────── */
  function isActive(menu) {
    var p = window.location.pathname;
    return menu.activePaths.some(function (ap) {
      return p === ap || p.startsWith(ap + '/') || p.startsWith(ap + '?');
    });
  }

  /* ── Build mega item ───────────────────────────────────────── */
  function buildItem(item) {
    var cls = 'mm-item'
      + (item.featured ? ' mm-item--featured' : '')
      + (item.alert    ? ' mm-item--alert'    : '');
    var a = el('a', cls);
    a.href = item.href;
    a.innerHTML = '<span class="mm-item-icon">' + item.icon + '</span>'
      + '<div class="mm-item-body">'
      + '<div class="mm-item-title">' + item.title + '</div>'
      + (item.desc ? '<div class="mm-item-desc">' + item.desc + '</div>' : '')
      + '</div>';
    return a;
  }

  /* ── Build mega panel ──────────────────────────────────────── */
  function buildMegaPanel(menu) {
    var inner = el('div', 'mm-panel-inner');
    var grid  = el('div', 'mm-grid mm-grid--' + menu.columns.length + 'col');

    menu.columns.forEach(function (col) {
      var colEl = el('div', 'mm-col');
      colEl.appendChild(el('div', 'mm-col-head', col.head));
      col.items.forEach(function (item) { colEl.appendChild(buildItem(item)); });
      grid.appendChild(colEl);
    });
    inner.appendChild(grid);

    if (menu.footer) {
      var footer = el('div', 'mm-panel-footer');
      menu.footer.forEach(function (btn) {
        var a = el('a', 'mm-footer-cta mm-footer-cta--' + btn.style, btn.label);
        a.href = btn.href;
        footer.appendChild(a);
      });
      inner.appendChild(footer);
    }

    var panel = el('div', 'mm-panel mm-panel--mega');
    panel.appendChild(inner);
    return panel;
  }

  /* ── Build dropdown panel ──────────────────────────────────── */
  function buildDropdownPanel(menu) {
    var inner = el('div', 'mm-panel-inner');
    var list  = el('div', 'mm-dropdown-list');
    menu.items.forEach(function (item) {
      var a = el('a', 'mm-dropdown-item');
      a.href = item.href;
      a.innerHTML = '<span class="mm-dropdown-icon">' + item.icon + '</span>' + item.title;
      list.appendChild(a);
    });
    inner.appendChild(list);
    var panel = el('div', 'mm-panel mm-panel--dropdown');
    panel.appendChild(inner);
    return panel;
  }

  /* ── Build the nav links ───────────────────────────────────── */
  function buildNav() {
    var navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    navLinks.innerHTML = '';

    MENU.forEach(function (menu) {
      var active  = isActive(menu);
      var isDrop  = menu.type === 'dropdown';
      var trigger = el('div', 'mm-trigger' + (isDrop ? ' mm-trigger--dropdown' : ''));

      var btn = el('button', 'mm-btn' + (active ? ' mm-active' : ''));
      btn.type = 'button';
      btn.innerHTML = menu.label + CHEVRON;
      trigger.appendChild(btn);

      var panel = isDrop ? buildDropdownPanel(menu) : buildMegaPanel(menu);
      trigger.appendChild(panel);
      navLinks.appendChild(trigger);
    });

    /* Add hamburger before the CTA */
    var navRight = document.querySelector('.nav-right');
    if (navRight && !navRight.querySelector('.mm-hamburger')) {
      var hb = el('button', 'mm-hamburger');
      hb.type = 'button';
      hb.setAttribute('aria-label', 'Open navigation');
      hb.innerHTML = '<span class="mm-hamburger-bar"></span>'
        + '<span class="mm-hamburger-bar"></span>'
        + '<span class="mm-hamburger-bar"></span>';
      hb.addEventListener('click', openDrawer);
      navRight.insertBefore(hb, navRight.firstChild);
    }

    buildMobileDrawer();
  }

  /* ── Mobile drawer ─────────────────────────────────────────── */
  function buildMobileDrawer() {
    if (document.querySelector('.mm-drawer')) return;

    var overlay = el('div', 'mm-overlay');
    overlay.addEventListener('click', closeDrawer);
    document.body.appendChild(overlay);

    var drawer = el('div', 'mm-drawer');
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-label', 'Navigation');
    drawer.innerHTML =
      '<div class="mm-drawer-head">'
      + '<span class="mm-drawer-title">Govisk ExecCom</span>'
      + '<button class="mm-drawer-close" type="button" aria-label="Close">&#x2715;</button>'
      + '</div>'
      + '<div class="mm-drawer-body">'
      + '<div class="mm-mobile-section">'
      + '<div class="mm-mobile-section-head">Intelligence</div>'
      + '<a class="mm-mobile-link" href="/portal"><span class="mm-mobile-icon">⚡</span>ExecCom Portal</a>'
      + '<a class="mm-mobile-link" href="/region/uk"><span class="mm-mobile-icon">🇬🇧</span>United Kingdom</a>'
      + '<a class="mm-mobile-link" href="/region/europe"><span class="mm-mobile-icon">🇪🇺</span>Europe</a>'
      + '<a class="mm-mobile-link" href="/region/north-america"><span class="mm-mobile-icon">🌎</span>North America</a>'
      + '<a class="mm-mobile-link" href="/region/latin-america"><span class="mm-mobile-icon">🌎</span>Latin America</a>'
      + '<a class="mm-mobile-link" href="/region/asia-pacific"><span class="mm-mobile-icon">🌏</span>Asia-Pacific</a>'
      + '<a class="mm-mobile-link" href="/region/africa"><span class="mm-mobile-icon">🌍</span>Africa</a>'
      + '</div>'
      + '<div class="mm-mobile-section">'
      + '<div class="mm-mobile-section-head">Reports</div>'
      + '<a class="mm-mobile-link" href="/portal?report=cass_health_check"><span class="mm-mobile-icon">📊</span>CASS Health Check</a>'
      + '<a class="mm-mobile-link" href="/portal?report=threat_intelligence"><span class="mm-mobile-icon">🎯</span>Threat Intelligence</a>'
      + '<a class="mm-mobile-link" href="/portal?report=cyber_threat_assessment"><span class="mm-mobile-icon">🛡</span>Cyber Assessment</a>'
      + '<a class="mm-mobile-link" href="/portal"><span class="mm-mobile-icon">📋</span>All Reports →</a>'
      + '</div>'
      + '<div class="mm-mobile-section">'
      + '<div class="mm-mobile-section-head">Compliance</div>'
      + '<a class="mm-mobile-link" href="/blacklist"><span class="mm-mobile-icon">🔴</span>FATF Blacklist</a>'
      + '<a class="mm-mobile-link" href="/grc-templates"><span class="mm-mobile-icon">📄</span>GRC Templates</a>'
      + '<a class="mm-mobile-link" href="/grc_dashboard"><span class="mm-mobile-icon">📊</span>GRC Dashboard</a>'
      + '</div>'
      + '<div class="mm-mobile-section">'
      + '<div class="mm-mobile-section-head">Company</div>'
      + '<a class="mm-mobile-link" href="/about"><span class="mm-mobile-icon">🏢</span>About Us</a>'
      + '<a class="mm-mobile-link" href="/services"><span class="mm-mobile-icon">⚙️</span>Services</a>'
      + '<a class="mm-mobile-link" href="/case-studies"><span class="mm-mobile-icon">📁</span>Case Studies</a>'
      + '<a class="mm-mobile-link" href="/contact"><span class="mm-mobile-icon">✉️</span>Contact Us</a>'
      + '</div>'
      + '<div class="mm-drawer-cta">'
      + '<a href="/request-demo" class="mm-drawer-cta-btn mm-drawer-cta-btn--primary">Request Demo</a>'
      + '<a href="/portal" class="mm-drawer-cta-btn mm-drawer-cta-btn--outline">Open Portal →</a>'
      + '</div>'
      + '</div>';

    drawer.querySelector('.mm-drawer-close').addEventListener('click', closeDrawer);
    document.body.appendChild(drawer);
  }

  function openDrawer() {
    var drawer  = document.querySelector('.mm-drawer');
    var overlay = document.querySelector('.mm-overlay');
    var hb      = document.querySelector('.mm-hamburger');
    if (drawer)  drawer.classList.add('mm-is-open');
    if (overlay) overlay.classList.add('mm-is-open');
    if (hb)      hb.classList.add('mm-is-open');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    var drawer  = document.querySelector('.mm-drawer');
    var overlay = document.querySelector('.mm-overlay');
    var hb      = document.querySelector('.mm-hamburger');
    if (drawer)  drawer.classList.remove('mm-is-open');
    if (overlay) overlay.classList.remove('mm-is-open');
    if (hb)      hb.classList.remove('mm-is-open');
    document.body.style.overflow = '';
  }

  /* ── Click-to-toggle (locks panel open; works on touch too) ── */
  function closeAll() {
    document.querySelectorAll('.mm-trigger.mm-is-open').forEach(function (t) {
      t.classList.remove('mm-is-open');
    });
  }

  function attachClickToggle(trigger, btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var wasOpen = trigger.classList.contains('mm-is-open');
      closeAll();
      if (!wasOpen) {
        trigger.classList.add('mm-is-open');
      }
    });
  }

  /* ── Boot ──────────────────────────────────────────────────── */
  function init() {
    buildNav();

    /* Wire click-toggle onto every trigger button */
    document.querySelectorAll('.mm-trigger .mm-btn').forEach(function (btn) {
      attachClickToggle(btn.closest('.mm-trigger'), btn);
    });

    /* Clicking outside any panel closes all */
    document.addEventListener('click', closeAll);

    /* Escape key closes all */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeAll();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
