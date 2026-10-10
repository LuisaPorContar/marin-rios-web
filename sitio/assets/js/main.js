/* Marín Ríos Consultores — interacciones */
(function () {
  'use strict';

  var sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Menú móvil ---- */
  var btnMenu = document.querySelector('.menu-btn');
  var nav = document.querySelector('.nav');
  if (btnMenu && nav) {
    btnMenu.addEventListener('click', function () {
      var abierto = nav.getAttribute('data-abierto') === 'true';
      nav.setAttribute('data-abierto', String(!abierto));
      btnMenu.setAttribute('aria-expanded', String(!abierto));
      btnMenu.setAttribute('aria-label', abierto ? 'Abrir menú' : 'Cerrar menú');
    });
  }

  /* ---- Submenú de servicios (clic en móvil, hover en escritorio) ---- */
  document.querySelectorAll('.nav__item').forEach(function (item) {
    var toggle = item.querySelector('.nav__toggle');
    if (!toggle) return;

    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      var abierto = item.getAttribute('data-abierto') === 'true';
      item.setAttribute('data-abierto', String(!abierto));
      toggle.setAttribute('aria-expanded', String(!abierto));
    });

    var escritorio = window.matchMedia('(min-width: 861px)');
    item.addEventListener('mouseenter', function () {
      if (escritorio.matches) item.setAttribute('data-abierto', 'true');
    });
    item.addEventListener('mouseleave', function () {
      if (escritorio.matches) item.setAttribute('data-abierto', 'false');
    });
  });

  /* Cerrar el menú al hacer clic fuera */
  document.addEventListener('click', function (e) {
    if (nav && btnMenu && !nav.contains(e.target) && !btnMenu.contains(e.target)) {
      nav.setAttribute('data-abierto', 'false');
      btnMenu.setAttribute('aria-expanded', 'false');
    }
  });

  /* ---- Sombra de la cabecera al desplazar ---- */
  var cabecera = document.querySelector('.cabecera');
  if (cabecera) {
    var alSubir = function () {
      cabecera.classList.toggle('cabecera--fija', window.scrollY > 12);
    };
    alSubir();
    window.addEventListener('scroll', alSubir, { passive: true });
  }

  /* ---- Acordeón de preguntas frecuentes ---- */
  document.querySelectorAll('.faq__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      var abierto = btn.getAttribute('aria-expanded') === 'true';

      // Solo una abierta a la vez dentro del mismo bloque
      var grupo = btn.closest('.faq');
      if (grupo && !abierto) {
        grupo.querySelectorAll('.faq__btn[aria-expanded="true"]').forEach(function (otro) {
          otro.setAttribute('aria-expanded', 'false');
          var p = document.getElementById(otro.getAttribute('aria-controls'));
          if (p) p.setAttribute('data-abierto', 'false');
        });
      }

      btn.setAttribute('aria-expanded', String(!abierto));
      if (panel) panel.setAttribute('data-abierto', String(!abierto));
    });
  });

  /* ---- Acordeón editorial ---- */
  document.querySelectorAll('.acordeon__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      var abierto = btn.getAttribute('aria-expanded') === 'true';
      var grupo = btn.closest('.acordeon');

      if (grupo && !abierto && grupo.getAttribute('data-multiple') !== 'true') {
        grupo.querySelectorAll('.acordeon__btn[aria-expanded="true"]').forEach(function (otro) {
          otro.setAttribute('aria-expanded', 'false');
          var p = document.getElementById(otro.getAttribute('aria-controls'));
          if (p) p.setAttribute('data-abierto', 'false');
        });
      }

      btn.setAttribute('aria-expanded', String(!abierto));
      if (panel) panel.setAttribute('data-abierto', String(!abierto));
    });
  });

  /* ---- Carruseles ---- */
  document.querySelectorAll('.carrusel').forEach(function (carrusel) {
    var pista = carrusel.querySelector('.carrusel__pista');
    var anterior = carrusel.querySelector('[data-dir="anterior"]');
    var siguiente = carrusel.querySelector('[data-dir="siguiente"]');
    var progreso = carrusel.querySelector('.carrusel__progreso i');
    if (!pista) return;

    function paso() {
      var primera = pista.firstElementChild;
      if (!primera) return pista.clientWidth;
      var gap = parseFloat(getComputedStyle(pista).columnGap) || 0;
      return primera.getBoundingClientRect().width + gap;
    }

    function actualizar() {
      var max = pista.scrollWidth - pista.clientWidth;
      var pos = pista.scrollLeft;
      if (anterior) anterior.disabled = pos < 4;
      if (siguiente) siguiente.disabled = pos > max - 4;

      if (progreso) {
        var visible = pista.clientWidth / pista.scrollWidth;
        var avance = max > 0 ? pos / max : 0;
        progreso.style.width = Math.max(visible * 100, 12) + '%';
        progreso.style.transform = 'translateX(' + (avance * (100 / Math.max(visible, .12) - 100)) + '%)';
      }
    }

    function mover(sentido) {
      pista.scrollBy({ left: sentido * paso(), behavior: sinMovimiento ? 'auto' : 'smooth' });
    }

    if (anterior) anterior.addEventListener('click', function () { mover(-1); });
    if (siguiente) siguiente.addEventListener('click', function () { mover(1); });
    pista.addEventListener('scroll', actualizar, { passive: true });
    window.addEventListener('resize', actualizar);

    /* Navegación con teclado dentro de la pista */
    pista.setAttribute('tabindex', '0');
    pista.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); mover(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); mover(-1); }
    });

    actualizar();
  });

  /* ---- Revelado al hacer scroll ---- */
  var objetivos = document.querySelectorAll('.revelar, .renglon');

  if (sinMovimiento || !('IntersectionObserver' in window)) {
    objetivos.forEach(function (el) { el.classList.add('visible'); });
  } else {
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add('visible');
        observador.unobserve(entrada.target);
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -60px 0px' });

    objetivos.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      observador.observe(el);
    });
  }

  /* ---- Año en el pie ---- */
  var anio = document.querySelector('[data-anio]');
  if (anio) anio.textContent = new Date().getFullYear();
})();
