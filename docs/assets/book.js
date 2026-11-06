/* Aiphabess book: page turning (StPageFlip, MIT), index tabs, page-stack thickness. */
(function () {
  var book = document.getElementById('book');
  var wrap = document.querySelector('.bookwrap');
  var pages = book.querySelectorAll('.page');
  var total = pages.length;

  // ?check : lay pages flat and flag any page whose content overflows (used by the build check)
  if (/[?&]check/.test(location.search)) {
    document.body.classList.add('check');
    var bad = [];
    pages.forEach(function (p, i) {
      var pc = p.querySelector('.pc');
      if (pc && pc.scrollHeight > pc.clientHeight + 2) { p.classList.add('flag'); bad.push(i + ':' + (pc.scrollHeight - pc.clientHeight)); }
    });
    var out = document.createElement('pre'); out.id = 'chk'; out.textContent = 'OVERFLOW[' + bad.join(',') + ']';
    document.body.appendChild(out);
    return;
  }

  var flip = new St.PageFlip(book, {
    width: 560, height: 780, size: 'stretch',
    minWidth: 260, maxWidth: 780, minHeight: 362, maxHeight: 1086,
    showCover: true, usePortrait: true, mobileScrollSupport: false,
    maxShadowOpacity: 0.55, flippingTime: 950, drawShadow: true, autoSize: true
  });
  flip.loadFromHTML(pages);

  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  var stackL = document.querySelector('.stack.l'), stackR = document.querySelector('.stack.r');

  function update(i) {
    var closed = i === 0 || i >= total - 1;
    wrap.classList.toggle('closed', i === 0);
    wrap.classList.toggle('closed-back', i >= total - 1);
    var frac = Math.min(1, Math.max(0, i / (total - 1)));
    var maxW = Math.max(4, Math.round(wrap.clientWidth * 0.012));
    stackL.style.setProperty('--w', Math.round(maxW * frac) + 'px');
    stackR.style.setProperty('--w', Math.round(maxW * (1 - frac)) + 'px');
    var cur = -1;
    tabs.forEach(function (t, k) {
      var p = +t.dataset.page;
      t.classList.toggle('passed', p <= i);
      if (p <= i + 1) cur = k;
    });
    tabs.forEach(function (t, k) { t.classList.toggle('on', k === cur && !closed); });
    if (history.replaceState) history.replaceState(null, '', i ? '#p' + i : location.pathname);
  }

  flip.on('flip', function (e) { update(e.data); });
  flip.on('init', function () { update(flip.getCurrentPageIndex()); });

  function go(n) { n = Math.max(0, Math.min(total - 1, n)); flip.flip(n); }
  tabs.forEach(function (t) { t.addEventListener('click', function () { go(+t.dataset.page); }); });
  document.querySelectorAll('[data-goto]').forEach(function (a) {
    a.addEventListener('click', function (ev) { ev.preventDefault(); ev.stopPropagation(); go(+a.dataset.goto); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') flip.flipNext();
    if (e.key === 'ArrowLeft') flip.flipPrev();
  });

  var m = /#p(\d+)/.exec(location.hash);
  if (m) flip.turnToPage(+m[1]);
  update(flip.getCurrentPageIndex());
})();
