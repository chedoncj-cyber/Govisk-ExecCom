(function() {
  var form = document.getElementById('login-form');
  var btn  = document.getElementById('submit-btn');
  var err  = document.getElementById('err');
  var next = new URLSearchParams(window.location.search).get('next') || '/portal';

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    err.style.display = 'none';

    var username = document.getElementById('username').value.trim();
    var password = document.getElementById('password').value;

    if (!username || !password) {
      err.textContent = 'Please enter your username and password.';
      err.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span>Signing in…';

    fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({ username: username, password: password }),
    }).then(function(res) {
      if (res.ok) {
        window.location.href = next;
      } else {
        return res.json().catch(function(){ return {}; }).then(function(data) {
          err.textContent = data.detail || 'Invalid credentials. Please try again.';
          err.style.display = 'block';
          btn.disabled = false;
          btn.textContent = 'Sign in';
          document.getElementById('password').value = '';
          document.getElementById('password').focus();
        });
      }
    }).catch(function() {
      err.textContent = 'Network error. Please check your connection and try again.';
      err.style.display = 'block';
      btn.disabled = false;
      btn.textContent = 'Sign in';
    });
  });
})();
