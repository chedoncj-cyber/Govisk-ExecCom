(function(){
  var btn=document.getElementById('nav-hamburger');
  var links=document.querySelector('.nav-links');
  if(btn&&links){links.id='nav-links';btn.addEventListener('click',function(){var open=links.classList.toggle('open');btn.classList.toggle('open',open);btn.setAttribute('aria-expanded',open);});document.addEventListener('click',function(e){if(!btn.contains(e.target)&&!links.contains(e.target)){links.classList.remove('open');btn.classList.remove('open');btn.setAttribute('aria-expanded','false');}});}
})();

(function(){
  var path = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.docs-nav-link[data-path]').forEach(function(a){
    var dp = a.getAttribute('data-path').split('#')[0].replace(/\/$/, '') || '/';
    if(dp === path) a.classList.add('active');
  });
  var inp = document.getElementById('docs-search-input');
  if(inp){
    inp.addEventListener('input', function(){
      var q = inp.value.toLowerCase();
      document.querySelectorAll('.docs-nav-link').forEach(function(a){
        a.style.display = (!q || a.textContent.toLowerCase().includes(q)) ? '' : 'none';
      });
      document.querySelectorAll('.docs-nav-section-title').forEach(function(t){
        var sec = t.closest('.docs-nav-section');
        if(!sec) return;
        var anyVisible = Array.from(sec.querySelectorAll('.docs-nav-link')).some(function(a){ return a.style.display !== 'none'; });
        sec.style.display = anyVisible ? '' : 'none';
      });
    });
  }
})();

(function(){
  var el = document.getElementById('ticker-date');
  if(el) el.textContent = new Date().toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'});
})();

(function() {
  var canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var W = window.innerWidth, H = window.innerHeight;
  canvas.width = W; canvas.height = H;
  window.addEventListener('resize', function(){ W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; });
  var pts = Array.from({length:40}, function(){ return {
    x:Math.random()*W, y:Math.random()*H,
    vx:(Math.random()-.5)*.25, vy:(Math.random()-.5)*.25,
    r:Math.random()*1+.3, a:Math.random()*.25+.04
  }; });
  (function draw() {
    ctx.clearRect(0,0,W,H);
    pts.forEach(function(p){
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0)p.x=W; if(p.x>W)p.x=0;
      if(p.y<0)p.y=H; if(p.y>H)p.y=0;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle='rgba(62,189,250,'+p.a+')'; ctx.fill();
    });
    for(var i=0;i<pts.length;i++) for(var j=i+1;j<pts.length;j++){
      var dx=pts[i].x-pts[j].x, dy=pts[i].y-pts[j].y, d=Math.sqrt(dx*dx+dy*dy);
      if(d<110){ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);
        ctx.strokeStyle='rgba(62,130,250,'+(.06*(1-d/110))+')';ctx.lineWidth=.5;ctx.stroke();}
    }
    requestAnimationFrame(draw);
  })();
})();

(function(){
  var b=document.getElementById('cookie-banner');
  if(!localStorage.getItem('cookie-consent')&&b){b.style.display='flex';}
  window.setCookieConsent=function(v){localStorage.setItem('cookie-consent',v);if(b)b.style.display='none';};
})();
