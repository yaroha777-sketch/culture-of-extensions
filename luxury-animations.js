/**
 * Culture of Extensions — Luxury Motion & Interactions Script
 * Features:
 *  1. Golden Reading Progress Bar
 *  2. Ambient Gold Follower Cursor Glow & Interactive Aura
 *  3. Magnetic Button Attraction
 *  4. Parallax Image & Section Mask Reveal (IntersectionObserver)
 */

(function () {
  'use strict';

  var isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Ensure CSS is loaded dynamically if not present
  function ensureCSS() {
    if (!document.querySelector('link[href*="luxury-animations.css"]')) {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = '/luxury-animations.css';
      document.head.appendChild(link);
    }
  }

  // --- 1. Reading Progress Bar ---
  function initProgressBar() {
    var progressBar = document.createElement('div');
    progressBar.id = 'lux-progress-bar';
    document.body.appendChild(progressBar);

    var ticking = false;
    function updateProgress() {
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = Math.min(100, Math.max(0, progress)) + '%';
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(updateProgress);
        ticking = true;
      }
    }, { passive: true });

    updateProgress();
  }

  // --- 2. Ambient Gold Cursor & Magnetic Buttons ---
  function initAmbientCursor() {
    if (isTouch || prefersReducedMotion) return;

    var cursor = document.createElement('div');
    cursor.id = 'lux-cursor-glow';
    document.body.appendChild(cursor);

    var mouseX = window.innerWidth / 2;
    var mouseY = window.innerHeight / 2;
    var currentX = mouseX;
    var currentY = mouseY;
    var isVisible = false;

    document.addEventListener('mousemove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!isVisible) {
        cursor.style.opacity = '1';
        isVisible = true;
      }
    }, { passive: true });

    document.addEventListener('mouseleave', function () {
      cursor.style.opacity = '0';
      isVisible = false;
    });

    function renderCursor() {
      currentX += (mouseX - currentX) * 0.12;
      currentY += (mouseY - currentY) * 0.12;
      cursor.style.left = currentX + 'px';
      cursor.style.top = currentY + 'px';
      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);

    // Hover detection for aura scaling
    var interactiveSelectors = 'a, button, .btn, .gallery-card, .card, input, summary, details';
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest(interactiveSelectors)) {
        document.body.classList.add('lux-cursor-hover');
      }
    }, { passive: true });

    document.addEventListener('mouseout', function (e) {
      if (e.target.closest(interactiveSelectors)) {
        document.body.classList.remove('lux-cursor-hover');
      }
    }, { passive: true });

    // Magnetic Buttons
    var magneticElements = document.querySelectorAll('.btn, nav.main a, header a.logo');
    magneticElements.forEach(function (elem) {
      elem.addEventListener('mousemove', function (e) {
        var rect = elem.getBoundingClientRect();
        var centerX = rect.left + rect.width / 2;
        var centerY = rect.top + rect.height / 2;
        var distanceX = e.clientX - centerX;
        var distanceY = e.clientY - centerY;

        elem.style.transform = 'translate(' + (distanceX * 0.22) + 'px, ' + (distanceY * 0.22) + 'px)';
      });

      elem.addEventListener('mouseleave', function () {
        elem.style.transform = 'translate(0px, 0px)';
      });
    });
  }

  // --- 3. Parallax Image Mask Reveal ---
  function initMaskReveal() {
    if (prefersReducedMotion) return;

    var targets = document.querySelectorAll('img, .gallery-card, .card, section, .hero-markup');
    targets.forEach(function (el) {
      if (el.closest('header') || el.closest('nav') || el.classList.contains('logo')) return;
      if (!el.classList.contains('lux-reveal') && !el.classList.contains('lux-reveal-fade')) {
        if (el.tagName === 'IMG' || el.classList.contains('gallery-card')) {
          el.classList.add('lux-reveal');
        } else {
          el.classList.add('lux-reveal-fade');
        }
      }
    });

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            obs.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.08,
        rootMargin: '0px 0px -40px 0px'
      });

      document.querySelectorAll('.lux-reveal, .lux-reveal-fade').forEach(function (el) {
        observer.observe(el);
      });
    } else {
      document.querySelectorAll('.lux-reveal, .lux-reveal-fade').forEach(function (el) {
        el.classList.add('is-revealed');
      });
    }
  }

  // --- Initialize on DOMContentLoaded ---
  function init() {
    ensureCSS();
    initProgressBar();
    initAmbientCursor();
    initMaskReveal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
