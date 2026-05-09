#!/usr/bin/env python3
"""Patch zaaack markdown-editor main.js to add: outline view, intra-doc anchor
nav, and Cmd+F find-in-page. Idempotent: re-running is safe."""
import os, sys

PATH = os.path.expanduser(
    '~/.vscode/extensions/zaaack.markdown-editor-0.1.13/media/dist/main.js'
)

with open(PATH) as f:
    src = f.read()

# ---- Patch 1: enable vditor outline view (default left-side panel) ----
P1_OLD = 'toolbarConfig:{pin:!0},'
P1_NEW = 'toolbarConfig:{pin:!0},outline:{enable:!0,position:"left"},'
if P1_NEW not in src:
    assert src.count(P1_OLD) == 1, 'P1 anchor not found or not unique'
    src = src.replace(P1_OLD, P1_NEW, 1)
    print('[1/3] outline option inserted')
else:
    print('[1/3] outline already enabled')

# ---- Patch 2: hook after() to call our enhancer ----
P2_OLD = 'after(){V_(),Y_(),sB(),K_()}'
P2_NEW = 'after(){V_(),Y_(),sB(),K_(),window.__zaaackEnhance&&window.__zaaackEnhance()}'
if P2_NEW not in src:
    assert src.count(P2_OLD) == 1, 'P2 anchor not found or not unique'
    src = src.replace(P2_OLD, P2_NEW, 1)
    print('[2/3] after() hook installed')
else:
    print('[2/3] after() hook already installed')

# ---- Patch 3: define window.__zaaackEnhance with anchor-nav + find-in-page ----
ENHANCE_MARKER = '/*__zaaackEnhance__*/'
ENHANCE_JS = ENHANCE_MARKER + r'''
window.__zaaackEnhance=function(){
  try {
    var ed = document.querySelector('#app');
    if (!ed || ed.__zaaackEnhanced) return;
    ed.__zaaackEnhanced = true;

    // ---- Intra-doc anchor link navigation ----
    function slug(s){ return (s||'').trim().toLowerCase().replace(/\s+/g,'-').replace(/[^\w\-]/g,''); }
    function findHeading(id) {
      try {
        var byId = ed.querySelector('[id="' + CSS.escape(id) + '"]');
        if (byId) return byId;
      } catch(_) {}
      var want = decodeURIComponent(id || '').toLowerCase();
      var hs = ed.querySelectorAll('h1,h2,h3,h4,h5,h6');
      for (var i = 0; i < hs.length; i++) {
        if (slug(hs[i].textContent) === slug(want)) return hs[i];
      }
      return null;
    }
    ed.addEventListener('click', function(e){
      var a = e.target && e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || href.length < 2) return;
      var t = findHeading(href.slice(1));
      if (!t) return;
      e.preventDefault();
      e.stopPropagation();
      t.scrollIntoView({behavior:'smooth', block:'start'});
    }, true);

    // ---- Cmd+F find-in-page overlay ----
    var bar = null, hits = [], idx = -1, lastQ = '';

    function clearHits(){
      hits.forEach(function(s){
        if (s.parentNode) s.parentNode.replaceChild(document.createTextNode(s.textContent), s);
      });
      hits = []; idx = -1;
    }

    function highlightCurrent(){
      hits.forEach(function(s,i){ s.style.background = (i===idx)?'#ff9800':'#ffd54f'; s.style.color='#000'; });
      if (idx >= 0 && hits[idx]) hits[idx].scrollIntoView({behavior:'smooth', block:'center'});
      if (bar) bar.querySelector('#__zk-count').textContent = hits.length ? (idx+1)+'/'+hits.length : '0/0';
    }

    function doFind(q, dir){
      clearHits();
      lastQ = q || '';
      if (!q) { if (bar) bar.querySelector('#__zk-count').textContent=''; return; }
      var re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      var walker = document.createTreeWalker(ed, NodeFilter.SHOW_TEXT, {
        acceptNode: function(n){
          if (!n.textContent || !n.textContent.replace(/\s/g,'')) return NodeFilter.FILTER_REJECT;
          var p = n.parentElement;
          while (p && p !== ed) {
            if (p.id === '__zk-bar') return NodeFilter.FILTER_REJECT;
            var cl = p.className || '';
            if (typeof cl === 'string' && /vditor-toolbar|vditor-outline|vditor-hint|vditor-panel/.test(cl)) {
              return NodeFilter.FILTER_REJECT;
            }
            p = p.parentElement;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      var nodes = [], n;
      while (n = walker.nextNode()) nodes.push(n);
      nodes.forEach(function(node){
        var text = node.textContent;
        var matches = [], m;
        while ((m = re.exec(text)) !== null) { matches.push({i:m.index,s:m[0]}); if (m.index === re.lastIndex) re.lastIndex++; }
        if (!matches.length) return;
        var frag = document.createDocumentFragment(), last = 0;
        matches.forEach(function(mm){
          if (mm.i > last) frag.appendChild(document.createTextNode(text.slice(last, mm.i)));
          var span = document.createElement('span');
          span.className = '__zk-hit';
          span.textContent = mm.s;
          frag.appendChild(span);
          hits.push(span);
          last = mm.i + mm.s.length;
        });
        if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
        if (node.parentNode) node.parentNode.replaceChild(frag, node);
      });
      if (hits.length) {
        idx = (dir < 0) ? hits.length - 1 : 0;
      }
      highlightCurrent();
    }

    function nextHit(dir){
      if (!hits.length) { doFind(lastQ, dir); return; }
      idx = ((idx + dir) % hits.length + hits.length) % hits.length;
      highlightCurrent();
    }

    function ensureBar(){
      if (bar) return bar;
      bar = document.createElement('div');
      bar.id = '__zk-bar';
      bar.style.cssText = 'position:fixed;top:6px;right:14px;z-index:99999;background:var(--vscode-editorWidget-background,#252526);color:var(--vscode-editorWidget-foreground,#ccc);border:1px solid var(--vscode-widget-border,var(--vscode-panel-border,#454545));padding:5px 7px;display:flex;gap:5px;align-items:center;font:12px -apple-system,system-ui,sans-serif;border-radius:3px;box-shadow:0 2px 8px rgba(0,0,0,0.4);';
      bar.innerHTML = '<input id="__zk-q" type="text" placeholder="Find" style="background:var(--vscode-input-background,#3c3c3c);color:var(--vscode-input-foreground,#cccccc);border:1px solid var(--vscode-input-border,#3c3c3c);padding:2px 6px;width:200px;outline:none;font:inherit;"/>'
        + '<span id="__zk-count" style="opacity:0.7;min-width:38px;text-align:center;"></span>'
        + '<button id="__zk-prev" title="Previous (Shift+Enter)" style="cursor:pointer;background:transparent;color:inherit;border:1px solid var(--vscode-widget-border,#454545);padding:1px 7px;font:inherit;">↑</button>'
        + '<button id="__zk-next" title="Next (Enter)" style="cursor:pointer;background:transparent;color:inherit;border:1px solid var(--vscode-widget-border,#454545);padding:1px 7px;font:inherit;">↓</button>'
        + '<button id="__zk-close" title="Close (Esc)" style="cursor:pointer;background:transparent;color:inherit;border:1px solid var(--vscode-widget-border,#454545);padding:1px 7px;font:inherit;">×</button>';
      document.body.appendChild(bar);
      var q = bar.querySelector('#__zk-q');
      bar.querySelector('#__zk-close').onclick = function(){ clearHits(); bar.style.display='none'; };
      bar.querySelector('#__zk-next').onclick = function(){ nextHit(1); };
      bar.querySelector('#__zk-prev').onclick = function(){ nextHit(-1); };
      var debTimer;
      q.addEventListener('input', function(){ clearTimeout(debTimer); debTimer = setTimeout(function(){ doFind(q.value, 0); }, 120); });
      q.addEventListener('keydown', function(e){
        if (e.key === 'Escape') { e.preventDefault(); clearHits(); bar.style.display='none'; }
        else if (e.key === 'Enter') { e.preventDefault(); if (q.value !== lastQ) { doFind(q.value, e.shiftKey?-1:1); } else { nextHit(e.shiftKey?-1:1); } }
      });
      return bar;
    }

    function openFind(){
      var b = ensureBar();
      b.style.display = 'flex';
      var q = b.querySelector('#__zk-q');
      q.focus(); q.select();
    }

    document.addEventListener('keydown', function(e){
      if ((e.metaKey || e.ctrlKey) && (e.key === 'f' || e.key === 'F')) {
        e.preventDefault(); e.stopPropagation();
        openFind();
      }
    }, true);
  } catch(err) { console.error('[zaaack patch]', err); }
};
'''

CLOSE = 'vscode.postMessage({command:"ready"});})();'
if ENHANCE_MARKER not in src:
    assert src.count(CLOSE) == 1, 'P3 anchor not found or not unique'
    # Inject before the final })();
    src = src.replace(CLOSE, 'vscode.postMessage({command:"ready"});' + ENHANCE_JS + '})();', 1)
    print('[3/3] __zaaackEnhance defined')
else:
    print('[3/3] __zaaackEnhance already defined')

with open(PATH, 'w') as f:
    f.write(src)
print('done')
