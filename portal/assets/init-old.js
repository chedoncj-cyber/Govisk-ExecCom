(function(){
  var btn = document.getElementById('nav-hamburger');
  var links = document.getElementById('nav-links');
  if (!btn || !links) return;
  btn.addEventListener('click', function(){
    var open = links.classList.toggle('open');
    btn.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
  });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape'){ links.classList.remove('open'); btn.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }});
})();

(function(){
  var b = document.getElementById('cookie-banner');
  if(b && localStorage.getItem('cba')) b.style.display = 'none';
})();
