// static/js/theme.js
(() => {
    const STORAGE_KEY = 'gaia-theme';
    const toggleEl = document.querySelector('.theme-toggle');
    const body = document.body;
  
    // pega tema salvo ou padrão
    const getPreferredTheme = () => localStorage.getItem(STORAGE_KEY) || 'light';
  
    // aplica tema mudando a classe do body
    const applyTheme = (theme) => {
      if (body.className != 'auth-page'){
        body.classList.remove('dark-mode', 'app-page');
        if (theme === 'dark'){
          body.classList.add('dark-mode'); // escuro
          if (toggleEl) toggleEl.classList.replace('fa-moon', 'fa-sun');
        } 
        else {
          body.classList.add('app-page'); // claro
          if (toggleEl) toggleEl.classList.replace('fa-sun', 'fa-moon');
        }}
    };
  
    // alterna ao clicar
    if (toggleEl) {
      toggleEl.addEventListener('click', () => {
        const current = getPreferredTheme();
        const next = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem(STORAGE_KEY, next);
        applyTheme(next);
      });
    }
  
    // aplica tema inicial
    applyTheme(getPreferredTheme());
  })();
  