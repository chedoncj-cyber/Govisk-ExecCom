/* ===== CASS Intelligence — Dual Globe Background ===== */
(function () {
  'use strict';

  const canvas = document.getElementById('globe-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H;
  let cxR, cyR, rR;
  let cxL, cyL, rL;
  let lastTs = null;

  // ── Hemisphere clip ──────────────────────────────────────────────────────────
  function clipHemi(pts) {
    if (!pts.length) return [];
    const out = [];
    for (let i = 0, n = pts.length; i < n; i++) {
      const a = pts[i], b = pts[(i + 1) % n];
      if (a.z >= 0) out.push(a);
      if ((a.z >= 0) !== (b.z >= 0)) {
        const t = a.z / (a.z - b.z);
        out.push({ x: a.x + t * (b.x - a.x), y: a.y + t * (b.y - a.y), z: 0 });
      }
    }
    return out;
  }

  function toSphere(lat, lng, rot) {
    const phi   = (90 - lat)  * Math.PI / 180;
    const theta = (lng + rot) * Math.PI / 180;
    return { x: Math.sin(phi)*Math.cos(theta), y: Math.cos(phi), z: Math.sin(phi)*Math.sin(theta) };
  }

  function proj(lat, lng, cx, cy, r, rot) {
    const p = toSphere(lat, lng, rot);
    return { sx: cx + p.x * r, sy: cy - p.y * r, z: p.z };
  }

  // ── Continent data ───────────────────────────────────────────────────────────
  const CONTINENTS = [
    {
      label: 'AFRICA', center: [0, 22],
      fill: 'rgba(180,83,9,0.22)', stroke: 'rgba(180,83,9,0.60)', lw: 1.0,
      coords: [
        [35.8,-5.9],[34.0,-6.8],[31.0,-9.8],[28.5,-12.5],[23.0,-16.5],
        [21.0,-17.0],[15.0,-17.5],[12.5,-16.8],[10.5,-15.0],[9.0,-13.5],
        [7.0,-11.5],[5.0,-5.5],[4.5,1.5],[4.0,2.5],[6.5,3.0],
        [4.0,6.5],[4.0,8.5],[2.0,9.5],[0.5,8.5],[0.0,9.0],
        [-1.0,9.3],[-3.0,10.0],[-5.0,12.0],[-6.0,12.2],[-8.5,13.0],
        [-15.0,12.0],[-17.0,11.8],[-22.5,14.5],[-28.5,16.5],
        [-33.5,18.5],[-34.5,20.0],[-34.0,26.0],[-30.0,30.5],
        [-26.0,32.5],[-22.0,35.5],[-18.0,37.5],[-15.0,40.5],
        [-10.0,40.5],[-7.0,39.5],[-4.5,39.5],[-2.0,41.0],
        [0.0,41.5],[2.0,41.0],[5.0,43.0],[10.0,44.0],[11.5,43.5],
        [15.0,41.5],[18.0,39.5],[20.0,37.5],[22.0,36.5],[24.0,35.0],
        [27.0,34.0],[30.0,32.5],[31.2,30.0],[31.0,25.0],[32.5,13.5],
        [37.0,10.0],[37.5,9.0],[36.5,5.0],[36.0,1.0],[35.8,-5.9]
      ]
    },
    {
      label: 'EUROPE', center: [54, 15],
      fill: 'rgba(29,107,181,0.20)', stroke: 'rgba(29,107,181,0.55)', lw: 1.0,
      coords: [
        [36.0,-9.0],[38.5,-1.5],[40.0,-0.5],[43.5,3.2],[43.5,7.5],
        [44.0,8.0],[44.5,12.0],[43.5,13.5],[40.5,14.5],[38.0,15.5],
        [40.0,18.5],[42.0,19.5],[42.0,22.0],[42.0,26.5],[42.0,28.0],
        [43.5,28.5],[44.0,28.8],[45.5,29.5],[46.5,30.5],[47.0,37.5],
        [42.0,43.5],[45.5,49.5],[47.5,53.5],[55.0,59.0],[60.0,28.0],
        [60.5,24.5],[65.0,25.5],[68.5,28.0],[70.5,28.0],[71.5,25.5],
        [71.5,22.0],[70.5,18.5],[68.0,14.0],[63.5,9.5],[62.0,5.5],
        [57.5,8.0],[56.0,10.5],[57.5,11.5],[55.5,12.5],[54.5,12.0],
        [54.0,10.0],[53.5,8.0],[52.5,5.0],[51.0,2.0],[50.5,0.0],
        [51.0,-2.0],[50.0,-5.5],[53.5,-10.0],[51.5,-10.0],[50.0,-10.0],
        [48.5,-4.5],[47.0,-2.0],[45.5,-1.0],[43.5,-1.5],[43.5,-4.0],
        [41.5,-8.5],[37.0,-7.5],[36.0,-9.0]
      ]
    },
    {
      label: 'ASIA', center: [45, 90],
      fill: 'rgba(14,116,144,0.18)', stroke: 'rgba(14,116,144,0.50)', lw: 1.0,
      coords: [
        [41,28],[41,36],[42,41],[43,47],[40,50],
        [37,54],[22,59],[23,57],[26,57],[23,68],
        [22,70],[20,73],[8,77],[8,80],[12,80],
        [16,82],[21,87],[22,92],[18,100],[5,100],
        [1,104],[11,107],[20,107],[22,114],[30,122],
        [35,120],[38,122],[42,130],[48,140],[52,141],
        [56,140],[60,162],[64,170],[68,162],[70,150],
        [73,120],[73,90],[73,73],[67,64],[60,60],
        [55,60],[50,58],[44,50],[42,41],[41,28]
      ]
    },
    {
      label: 'N. AMERICA', center: [45, -100],
      fill: 'rgba(22,163,74,0.18)', stroke: 'rgba(22,163,74,0.50)', lw: 1.0,
      coords: [
        [71,-141],[65,-168],[57,-153],[58,-137],[55,-130],
        [49,-124],[40,-124],[37,-122],[32,-117],[22,-106],
        [15,-93],[9,-79],[10,-75],[12,-72],[18,-66],
        [25,-77],[25,-80],[30,-81],[35,-76],[41,-70],
        [44,-63],[47,-53],[52,-56],[58,-62],[62,-78],
        [65,-83],[68,-87],[72,-80],[76,-82],[80,-95],
        [80,-115],[72,-128],[70,-135],[71,-141]
      ]
    },
    {
      label: 'L. AMERICA', center: [-15, -58],
      fill: 'rgba(22,163,74,0.18)', stroke: 'rgba(22,163,74,0.50)', lw: 1.0,
      coords: [
        [12,-72],[11,-64],[6,-61],[4,-52],[0,-51],
        [-3,-39],[-8,-35],[-13,-38],[-20,-40],[-23,-43],
        [-29,-50],[-33,-53],[-38,-57],[-41,-63],[-47,-66],
        [-52,-69],[-55,-67],[-50,-68],[-46,-75],[-38,-73],
        [-30,-71],[-22,-70],[-18,-70],[-8,-80],[-2,-81],
        [0,-80],[4,-77],[8,-77],[10,-75],[12,-72]
      ]
    },
    {
      label: 'AUSTRALIA', center: [-25, 133],
      fill: 'rgba(14,116,144,0.20)', stroke: 'rgba(14,116,144,0.52)', lw: 1.0,
      coords: [
        [-14,130],[-14.5,129],[-15,128.5],[-14.5,127],[-15.5,124.5],
        [-16.5,123.5],[-19.5,122],[-20.5,120],[-22,114],
        [-25.5,113.5],[-26.5,114],[-29.5,115],[-32,115.5],
        [-34.5,116],[-35.5,117.5],[-34.5,119],[-34,122.5],[-33.5,124],
        [-33,126],[-33.5,134.5],[-33.5,135.5],[-32.5,137],
        [-35,138.5],[-37.5,140],[-38.5,141.5],[-39,146.5],
        [-37,149.5],[-36.5,150.5],[-34,151.5],[-31,153],
        [-27.5,153.5],[-24.5,151.5],[-22,150],[-20.5,149],
        [-18.5,146.5],[-16.5,145.5],[-15,145.5],[-13.5,143.5],
        [-13,141],[-13.5,136.5],[-14,135.5],[-14.5,135],[-14,133.5],
        [-14,130]
      ]
    },
    {
      label: 'ANTARCT.', center: [-75, 0],
      fill: 'rgba(148,163,184,0.18)', stroke: 'rgba(148,163,184,0.40)', lw: 0.8,
      coords: (function () {
        const pts = [];
        for (let lng = -180; lng <= 180; lng += 10) pts.push([-65, lng]);
        pts.push([-65, -180]);
        return pts;
      }())
    }
  ];

  // ── Regional intelligence hubs ───────────────────────────────────────────────
  const HUBS = [
    { lat: 51.5,  lng:   0.1, label: 'London'    },
    { lat: 40.7,  lng: -74.0, label: 'New York'  },
    { lat: 25.2,  lng:  55.3, label: 'Dubai'     },
    { lat:  6.5,  lng:   3.4, label: 'Lagos'     },
    { lat:  1.3,  lng: 103.8, label: 'Singapore' },
    { lat: -23.5, lng: -46.6, label: 'São Paulo' },
    { lat: 50.1,  lng:   8.7, label: 'Frankfurt' },
  ];

  const CONNECTIONS = [
    [0, 1, 0.00], [0, 6, 0.15], [0, 2, 0.30], [0, 3, 0.45],
    [1, 5, 0.60], [2, 3, 0.10], [2, 4, 0.25], [6, 2, 0.70],
    [4, 1, 0.40], [3, 5, 0.80],
  ];

  // ── Sphere helpers ───────────────────────────────────────────────────────────
  function toSphere0(lat, lng) {
    var phi = (90 - lat) * Math.PI / 180;
    var tht = lng * Math.PI / 180;
    return { x: Math.sin(phi)*Math.cos(tht), y: Math.cos(phi), z: Math.sin(phi)*Math.sin(tht) };
  }

  function applyRotY(p, rotDeg) {
    var r = rotDeg * Math.PI / 180;
    var c = Math.cos(r), s = Math.sin(r);
    return { x: p.x*c + p.z*s, y: p.y, z: -p.x*s + p.z*c };
  }

  function slerpUnit(a, b, t) {
    var dot   = Math.max(-1, Math.min(1, a.x*b.x + a.y*b.y + a.z*b.z));
    var omega = Math.acos(dot);
    if (omega < 0.0001) return { x: a.x, y: a.y, z: a.z };
    var s = Math.sin(omega);
    return {
      x: (Math.sin((1-t)*omega)/s)*a.x + (Math.sin(t*omega)/s)*b.x,
      y: (Math.sin((1-t)*omega)/s)*a.y + (Math.sin(t*omega)/s)*b.y,
      z: (Math.sin((1-t)*omega)/s)*a.z + (Math.sin(t*omega)/s)*b.z
    };
  }

  // ── Currency train lanes — brighter RGB values ───────────────────────────────
  const LANES = [
    {
      lat: 0,  dir:  1, speed: 14, rot: 0,
      rgb: '56,189,248',           // sky blue
      syms: ['$','€','£','¥','₹','₩','Fr','₦','₺','₽','₿','฿','R$','kr','A$','C$','Rp','₱','৳','RM']
    },
    {
      lat: 30, dir: -1, speed: 10, rot: 90,
      rgb: '74,222,128',           // bright green
      syms: ['€','£','¥','₹','₩','Fr','₦','₺','₽','A$','C$','$']
    },
    {
      lat: -30, dir: 1, speed: 7, rot: 200,
      rgb: '251,146,60',           // bright amber
      syms: ['R','A$','C$','Rp','₱','₴','৳','RM','$','€','£']
    }
  ];

  // ── Grid helpers ─────────────────────────────────────────────────────────────
  function latCircle(lat, cx, cy, r, rot, stroke, lw) {
    ctx.beginPath(); ctx.strokeStyle = stroke; ctx.lineWidth = lw;
    let pen = false;
    for (let i = 0; i <= 120; i++) {
      const p = proj(lat, (i / 120) * 360 - 180, cx, cy, r, rot);
      if (p.z >= 0) { pen ? ctx.lineTo(p.sx, p.sy) : ctx.moveTo(p.sx, p.sy); pen = true; }
      else pen = false;
    }
    ctx.stroke();
  }

  function lngCircle(lng, cx, cy, r, rot, stroke, lw) {
    ctx.beginPath(); ctx.strokeStyle = stroke; ctx.lineWidth = lw;
    let pen = false;
    for (let i = 0; i <= 60; i++) {
      const p = proj((i / 60) * 180 - 90, lng, cx, cy, r, rot);
      if (p.z >= 0) { pen ? ctx.lineTo(p.sx, p.sy) : ctx.moveTo(p.sx, p.sy); pen = true; }
      else pen = false;
    }
    ctx.stroke();
  }

  // ── Hub connections ──────────────────────────────────────────────────────────
  function drawHubConnections(rot, ts) {
    var ARC_STEPS = 48;

    CONNECTIONS.forEach(function(conn) {
      var A0 = toSphere0(HUBS[conn[0]].lat, HUBS[conn[0]].lng);
      var B0 = toSphere0(HUBS[conn[1]].lat, HUBS[conn[1]].lng);
      var prev = null;

      for (var i = 0; i <= ARC_STEPS; i++) {
        var t  = i / ARC_STEPS;
        var p0 = slerpUnit(A0, B0, t);
        var p  = applyRotY(p0, rot);
        var sx = cxR + p.x * rR, sy = cyR - p.y * rR;
        if (prev !== null) {
          var avgZ = (prev.z + p.z) * 0.5;
          if (avgZ > -0.05) {
            var alpha = Math.max(0, avgZ) * 0.55 + 0.08;
            ctx.beginPath();
            ctx.moveTo(prev.sx, prev.sy);
            ctx.lineTo(sx, sy);
            ctx.strokeStyle = 'rgba(160,220,255,' + alpha.toFixed(3) + ')';
            ctx.lineWidth = 1.1;
            ctx.stroke();
          }
        }
        prev = { sx, sy, z: p.z };
      }

      // Animated packet + trail
      var speed = 0.00022;
      var tPkt  = ((ts * speed) + conn[2]) % 1;
      var TRAIL = 6;
      for (var ti = TRAIL; ti >= 0; ti--) {
        var tT  = (tPkt - ti * 0.012 + 1) % 1;
        var pT0 = slerpUnit(A0, B0, tT);
        var pT  = applyRotY(pT0, rot);
        if (pT.z < 0) continue;
        var depth = Math.max(0, pT.z);
        var frac  = 1 - ti / (TRAIL + 1);
        var dotA  = depth * frac * (ti === 0 ? 1.0 : 0.5);
        var dotR  = ti === 0 ? 3.8 : 1.8 * frac;
        var sxT   = cxR + pT.x * rR, syT = cyR - pT.y * rR;
        if (ti === 0) {
          var grd = ctx.createRadialGradient(sxT, syT, 0, sxT, syT, 12);
          grd.addColorStop(0, 'rgba(180,235,255,' + (dotA * 0.85).toFixed(3) + ')');
          grd.addColorStop(1, 'rgba(180,235,255,0)');
          ctx.beginPath(); ctx.arc(sxT, syT, 12, 0, Math.PI * 2);
          ctx.fillStyle = grd; ctx.fill();
        }
        ctx.beginPath();
        ctx.arc(sxT, syT, dotR, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,255,255,' + dotA.toFixed(3) + ')';
        ctx.fill();
      }
    });

    // Hub dots + city name labels
    HUBS.forEach(function(hub) {
      var p0    = toSphere0(hub.lat, hub.lng);
      var p     = applyRotY(p0, rot);
      if (p.z < -0.05) return;
      var depth = Math.max(0, p.z);
      var sx    = cxR + p.x * rR, sy = cyR - p.y * rR;
      var pulse = 0.5 + 0.5 * Math.sin(ts * 0.0025 + p0.x * 10);

      // Pulse ring
      ctx.beginPath();
      ctx.arc(sx, sy, 6 + pulse * 6, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(180,235,255,' + (depth * 0.38).toFixed(3) + ')';
      ctx.lineWidth = 0.9;
      ctx.stroke();

      // Outer glow
      var g = ctx.createRadialGradient(sx, sy, 0, sx, sy, 14);
      g.addColorStop(0, 'rgba(160,220,255,' + (depth * 0.70).toFixed(3) + ')');
      g.addColorStop(1, 'rgba(160,220,255,0)');
      ctx.beginPath(); ctx.arc(sx, sy, 14, 0, Math.PI * 2);
      ctx.fillStyle = g; ctx.fill();

      // Core dot
      ctx.beginPath();
      ctx.arc(sx, sy, 3.2, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,' + (depth * 0.98).toFixed(3) + ')';
      ctx.fill();

      // City label — only draw when clearly visible
      if (depth > 0.12) {
        var labelAlpha = Math.min(1, (depth - 0.12) / 0.20);
        var labelSz    = Math.max(9, rR * 0.032);
        ctx.save();
        ctx.font         = '700 ' + labelSz + 'px \'IBM Plex Sans\',\'Inter\',sans-serif';
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'top';
        // Dark outline for contrast against globe
        ctx.shadowColor  = 'rgba(0,10,30,0.95)';
        ctx.shadowBlur   = 6;
        ctx.fillStyle    = 'rgba(255,255,255,' + labelAlpha.toFixed(3) + ')';
        ctx.fillText(hub.label, sx, sy + 8);
        // Second pass: crisp white on top
        ctx.shadowBlur   = 0;
        ctx.fillStyle    = 'rgba(255,255,255,' + (labelAlpha * 0.90).toFixed(3) + ')';
        ctx.fillText(hub.label, sx, sy + 8);
        ctx.restore();
      }
    });
  }

  // ── Continent globe (RIGHT) ──────────────────────────────────────────────────
  function drawContinent(c, rot, fillOvr, strokeOvr, lwOvr) {
    const pts3d   = c.coords.map(([lat, lng]) => toSphere(lat, lng, rot));
    const clipped = clipHemi(pts3d);
    if (clipped.length < 3) return;
    ctx.beginPath();
    clipped.forEach((p, i) => {
      const sx = cxR + p.x * rR, sy = cyR - p.y * rR;
      i === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
    });
    ctx.closePath();
    ctx.fillStyle   = fillOvr   !== undefined ? fillOvr   : c.fill;
    ctx.fill();
    ctx.strokeStyle = strokeOvr !== undefined ? strokeOvr : c.stroke;
    ctx.lineWidth   = lwOvr     !== undefined ? lwOvr     : c.lw;
    ctx.stroke();
  }

  function drawContinentLabel(c, rot) {
    const p = proj(c.center[0], c.center[1], cxR, cyR, rR, rot);
    if (p.z < 0.10) return;
    const alpha = Math.min(1, (p.z - 0.10) / 0.18);
    const sz    = Math.max(10, rR * 0.036);

    ctx.save();
    ctx.font         = '800 ' + sz + 'px \'IBM Plex Sans\',\'Inter\',sans-serif';
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';
    // Bold dark halo for contrast against ocean/land
    ctx.shadowColor  = 'rgba(0,8,24,0.98)';
    ctx.shadowBlur   = 8;
    ctx.fillStyle    = 'rgba(255,255,255,' + alpha.toFixed(3) + ')';
    ctx.fillText(c.label, p.sx, p.sy);
    // Second crisp pass
    ctx.shadowBlur   = 0;
    ctx.fillStyle    = 'rgba(255,255,255,' + (alpha * 0.92).toFixed(3) + ')';
    ctx.fillText(c.label, p.sx, p.sy);
    ctx.restore();
  }

  function drawContinentGlobe(rot, ts) {
    ctx.save();
    ctx.beginPath(); ctx.arc(cxR, cyR, rR, 0, Math.PI * 2); ctx.clip();

    // Ocean sphere gradient
    const sg = ctx.createRadialGradient(
      cxR - rR * 0.32, cyR - rR * 0.32, rR * 0.04,
      cxR, cyR, rR
    );
    sg.addColorStop(0,    '#c2ebff');
    sg.addColorStop(0.42, '#4ab2e8');
    sg.addColorStop(1,    '#1a68b8');
    ctx.beginPath(); ctx.arc(cxR, cyR, rR, 0, Math.PI * 2);
    ctx.fillStyle = sg; ctx.fill();

    // Grid lines
    for (let lat = -80; lat <= 80; lat += 20)
      latCircle(lat, cxR, cyR, rR, rot, 'rgba(255,255,255,0.22)', 0.6);
    for (let lng = 0; lng < 360; lng += 20)
      lngCircle(lng, cxR, cyR, rR, rot, 'rgba(255,255,255,0.22)', 0.6);

    // Continents
    CONTINENTS.forEach(c => {
      const ice = c.label === 'ANTARCT.';
      drawContinent(c, rot,
        ice ? 'rgba(210,238,255,0.92)' : 'rgba(56,142,60,0.88)',
        ice ? 'rgba(180,215,245,0.76)' : 'rgba(27,94,32,0.85)',
        0.8
      );
    });

    // Continent labels
    CONTINENTS.forEach(c => drawContinentLabel(c, rot));

    // Equator line
    latCircle(0, cxR, cyR, rR, rot, 'rgba(255,255,255,0.50)', 1.3);

    // Hub arcs + packets + city labels
    drawHubConnections(rot, ts);

    // Specular glint
    const hg = ctx.createRadialGradient(
      cxR - rR * 0.32, cyR - rR * 0.32, 0,
      cxR - rR * 0.32, cyR - rR * 0.32, rR * 0.65
    );
    hg.addColorStop(0, 'rgba(255,255,255,0.24)');
    hg.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.beginPath(); ctx.arc(cxR, cyR, rR, 0, Math.PI * 2);
    ctx.fillStyle = hg; ctx.fill();

    ctx.restore();

    // Atmosphere glow
    const ag = ctx.createRadialGradient(cxR, cyR, rR * 0.80, cxR, cyR, rR * 1.12);
    ag.addColorStop(0, 'rgba(80,170,240,0)');
    ag.addColorStop(1, 'rgba(80,170,240,0.35)');
    ctx.beginPath(); ctx.arc(cxR, cyR, rR * 1.12, 0, Math.PI * 2);
    ctx.fillStyle = ag; ctx.fill();

    // Sphere border
    ctx.beginPath(); ctx.arc(cxR, cyR, rR, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(120,200,255,0.60)'; ctx.lineWidth = 1.8; ctx.stroke();
  }

  // ── Currency globe (LEFT) ────────────────────────────────────────────────────
  function drawCurrencyGlobe(rot) {
    // Ocean disc
    ctx.beginPath(); ctx.arc(cxL, cyL, rL, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(29,107,181,0.07)'; ctx.fill();

    // Grid
    for (let lat = -80; lat <= 80; lat += 20)
      latCircle(lat, cxL, cyL, rL, rot, 'rgba(56,189,248,0.10)', 0.5);
    for (let lng = 0; lng < 360; lng += 20)
      lngCircle(lng, cxL, cyL, rL, rot, 'rgba(56,189,248,0.10)', 0.5);

    // Orbit track dashes
    LANES.forEach(lane => {
      ctx.setLineDash([2, 6]);
      latCircle(lane.lat, cxL, cyL, rL, rot, `rgba(${lane.rgb},0.28)`, 0.9);
      ctx.setLineDash([]);
    });

    // Back-half ghost symbols (faded, receding side)
    LANES.forEach(lane => {
      const n = lane.syms.length;
      lane.syms.forEach((sym, i) => {
        const p = proj(lane.lat, (i / n) * 360 + lane.rot, cxL, cyL, rL, rot);
        if (p.z >= -0.04 || p.z < -0.55) return;
        const a  = (0.55 + p.z) * 0.28;
        const sz = rL * 0.072 * (0.45 + (p.z + 0.55) * 0.2);
        ctx.save();
        ctx.font         = '700 ' + sz + 'px \'IBM Plex Mono\',monospace';
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'middle';
        ctx.strokeStyle  = `rgba(180,0,0,${(a * 0.6).toFixed(3)})`;
        ctx.lineWidth    = Math.max(0.5, sz * 0.06);
        ctx.lineJoin     = 'round';
        ctx.strokeText(sym, p.sx, p.sy);
        ctx.fillStyle    = `rgba(0,0,0,${a.toFixed(3)})`;
        ctx.fillText(sym, p.sx, p.sy);
        ctx.restore();
      });
    });

    // Equator
    latCircle(0, cxL, cyL, rL, rot, 'rgba(56,189,248,0.30)', 1.1);

    // Front-half currency symbols — black fill, red outline
    LANES.forEach(lane => {
      const n = lane.syms.length;
      const visible = [];
      lane.syms.forEach((sym, i) => {
        const p = proj(lane.lat, (i / n) * 360 + lane.rot, cxL, cyL, rL, rot);
        if (p.z >= -0.04) visible.push({ sym, p });
      });

      // Connecting rail
      if (visible.length > 1) {
        ctx.beginPath();
        ctx.strokeStyle = 'rgba(200,0,0,0.20)';
        ctx.lineWidth = 1.2;
        visible.forEach((v, vi) => vi === 0 ? ctx.moveTo(v.p.sx, v.p.sy) : ctx.lineTo(v.p.sx, v.p.sy));
        ctx.stroke();
      }

      visible.forEach(({ sym, p }) => {
        const depth  = Math.max(0, p.z);
        const alpha  = 0.55 + depth * 0.45;        // solid from 0.55 upward
        const sz     = rL * 0.095 * (0.65 + depth * 0.35);
        const outW   = Math.max(1.2, sz * 0.10);   // red outline weight scales with font

        ctx.save();
        ctx.font         = '800 ' + sz + 'px \'IBM Plex Mono\',monospace';
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'middle';
        ctx.lineJoin     = 'round';

        // Red outline pass
        ctx.strokeStyle  = `rgba(220,0,0,${alpha.toFixed(3)})`;
        ctx.lineWidth    = outW;
        ctx.strokeText(sym, p.sx, p.sy);

        // Black fill pass
        ctx.fillStyle    = `rgba(0,0,0,${alpha.toFixed(3)})`;
        ctx.fillText(sym, p.sx, p.sy);
        ctx.restore();
      });
    });

    // Rim glow
    const g = ctx.createRadialGradient(cxL, cyL, rL * 0.80, cxL, cyL, rL * 1.04);
    g.addColorStop(0, 'rgba(56,189,248,0.00)');
    g.addColorStop(1, 'rgba(56,189,248,0.18)');
    ctx.beginPath(); ctx.arc(cxL, cyL, rL, 0, Math.PI * 2);
    ctx.fillStyle = g; ctx.fill();
    ctx.beginPath(); ctx.arc(cxL, cyL, rL, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(56,189,248,0.25)'; ctx.lineWidth = 1.2; ctx.stroke();

    // "WORLD CURRENCIES" label — bright and clear
    const sz = Math.max(10, rL * 0.055);
    ctx.save();
    ctx.font         = '700 ' + sz + 'px \'IBM Plex Sans\',\'Inter\',sans-serif';
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'top';
    ctx.shadowColor  = 'rgba(0,8,24,0.95)';
    ctx.shadowBlur   = 6;
    ctx.fillStyle    = 'rgba(186,230,253,0.92)';   // bright sky-blue-100
    ctx.fillText('WORLD CURRENCIES', cxL, cyL + rL + 12);
    ctx.shadowBlur   = 0;
    ctx.fillText('WORLD CURRENCIES', cxL, cyL + rL + 12);
    ctx.restore();
  }

  // ── Layout ───────────────────────────────────────────────────────────────────
  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    cxR = W > 860 ? W * 0.78 : W * 0.5;
    cyR = H * 0.5;
    rR  = Math.min(W, H) * (W > 860 ? 0.36 : 0.42);
    cxL = W * 0.16;
    cyL = H * 0.5;
    rL  = Math.min(W, H) * 0.24;
  }

  // ── Main loop ────────────────────────────────────────────────────────────────
  function frame(ts) {
    if (lastTs === null) lastTs = ts;
    const dt = Math.min((ts - lastTs) / 1000, 0.05);
    lastTs = ts;

    LANES.forEach(lane => { lane.rot += lane.dir * lane.speed * dt; });

    ctx.clearRect(0, 0, W, H);

    const rotR = ts * 0.010;
    const rotL = ts * 0.007;

    if (W > 860) drawCurrencyGlobe(rotL);
    drawContinentGlobe(rotR, ts);

    requestAnimationFrame(frame);
  }

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(frame);
})();
