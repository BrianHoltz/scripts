#!/usr/bin/env python3
"""Patch zaaack markdown-editor main.js to add: outline view, intra-doc anchor
nav, and Cmd+F find-in-page. Idempotent: re-running is safe.

Patches every installed copy under both ~/.vscode/extensions and
~/.cursor/extensions automatically (each IDE has its own extensions dir).
After running, reload each affected window (Developer: Reload Window).
"""
import os, sys, glob

CANDIDATE_GLOBS = [
    '~/.vscode/extensions/zaaack.markdown-editor-*/media/dist/main.js',
    '~/.cursor/extensions/zaaack.markdown-editor-*/media/dist/main.js',
]

# ---- Patch 1: enable vditor outline view (default left-side panel) ----
P1_OLD = 'toolbarConfig:{pin:!0},'
P1_NEW = 'toolbarConfig:{pin:!0},outline:{enable:!0,position:"left"},'

# ---- Patch 2: hook after() to call our enhancer ----
P2_OLD = 'after(){V_(),Y_(),sB(),K_()}'
P2_NEW = 'after(){V_(),Y_(),sB(),K_(),window.__zaaackEnhance&&window.__zaaackEnhance()}'

# ---- Patch 4: wrap vscode.postMessage to drop intra-doc open-link messages.
# Vditor's G_() click handler sends {command:"open-link",href:a.href} for
# any anchor click (using the *resolved* URL). For <a href="#section"> the
# resolved URL becomes <baseHref>#section (a non-http URL with fragment).
# The extension then path.resolve()s that to a directory + fragment and
# opens it as a file -> "directory cannot be viewed" error. We intercept
# postMessage and reroute hash-fragment opens to scroll the matching heading. ----
P4_OLD = 'window.vscode=window.acquireVsCodeApi&&window.acquireVsCodeApi();window.global=window;'
P4_MARKER = '/*__zk_postwrap__*/'
P4_NEW = (
    'window.vscode=window.acquireVsCodeApi&&window.acquireVsCodeApi();'
    + P4_MARKER
    + 'if(window.vscode&&!window.vscode.__zk_wrapped){'
      'var __zk_origPost=window.vscode.postMessage.bind(window.vscode);'
      'window.vscode.postMessage=function(m){'
        'try{'
          'if(m&&m.command==="open-link"&&typeof m.href==="string"&&!/^https?:/i.test(m.href)){'
            'var hi=m.href.indexOf("#");'
            'if(hi>=0){'
              'if(window.__zaaackGotoAnchor)window.__zaaackGotoAnchor(m.href.slice(hi+1));'
              'return;'
            '}'
          '}'
        '}catch(err){console.error("[zaaack-patch postMessage wrap]",err);}'
        'return __zk_origPost(m);'
      '};'
      'window.vscode.__zk_wrapped=true;'
    '}'
    'window.global=window;'
)

# ---- Patch 3: define window.__zaaackEnhance with anchor-nav + find-in-page ----
ENHANCE_MARKER = '/*__zaaackEnhance__*/'
ENHANCE_JS = ENHANCE_MARKER + r'''
// Heading lookup + scroll helper, exposed globally so the postMessage wrap
// can also use it.
//
// Vditor IR mode renders headings with marker spans inside the <h*>:
//   <h2 data-block="0">
//     <span class="vditor-ir__marker vditor-ir__marker--heading">## </span>
//     History
//   </h2>
// so .textContent includes "## History" — we have to skip marker spans
// when slugifying. Headings also often have NO id attribute in IR mode.
function slugify(s){
  return decodeURIComponent(s||'')
    .trim().toLowerCase()
    .replace(/^[#*\-_\s]+/,'')           // strip leading markdown markers
    .replace(/\s+/g,'-')
    .replace(/[^\w\-]/g,'');
}
function headingText(h){
  var out = '';
  for (var i=0;i<h.childNodes.length;i++){
    var n = h.childNodes[i];
    if (n.nodeType === 3) { out += n.nodeValue || ''; continue; }
    if (n.nodeType !== 1) continue;
    var cls = n.className || '';
    if (typeof cls === 'string' && /vditor-ir__marker/.test(cls)) continue;
    out += n.textContent || '';
  }
  return out;
}
window.__zaaackGotoAnchor = function(frag){
  if (!frag) return false;
  // Vditor renders inside .vditor-ir or similar; #app contains the toolbar
  // too. Try a few container selectors.
  var ed = document.querySelector('.vditor-ir__content')
        || document.querySelector('.vditor-ir')
        || document.querySelector('.vditor-reset')
        || document.querySelector('#app')
        || document.body;
  if (!ed) return false;
  var t = null;
  // 1) Direct id match
  try { t = ed.querySelector('[id="' + (window.CSS && CSS.escape ? CSS.escape(frag) : frag) + '"]'); } catch(_){}
  // 2) Heading text-slug match (skipping vditor marker spans)
  if (!t) {
    var want = slugify(frag);
    var hs = ed.querySelectorAll('h1,h2,h3,h4,h5,h6');
    for (var i=0;i<hs.length;i++){
      var s = slugify(headingText(hs[i]));
      if (s === want){ t = hs[i]; break; }
    }
  }
  if (!t) {
    console.warn('[zaaack-patch] no anchor match for', frag);
    return false;
  }
  t.scrollIntoView({behavior:'smooth', block:'start'});
  return true;
};

window.__zaaackEnhance=function(){
  try {
    var ed = document.querySelector('#app');
    if (!ed || ed.__zaaackEnhanced) return;
    ed.__zaaackEnhanced = true;

    // ---- Intra-doc anchor link navigation ----
    // VS Code webviews have a *built-in* link-click handler that fires
    // `did-click-link` to the workbench when an iframe attempts to navigate
    // to a non-http URL — that path lands in `openCodeEditor` and tries to
    // open the resolved directory as a text editor (-> "directories can't
    // be viewed in the IDE" error). The extension's `open-link` postMessage
    // path is a *separate* path (caught by our P4 postMessage wrap). To
    // stop the webview's built-in path we must call e.preventDefault() on
    // the click event in the inner document, BEFORE the iframe nav fires.
    function clickHandler(e){
      var t = e.target;
      if (!t) return;
      // 1) Real <a> elements (preview mode and any standard anchor)
      var a = t.closest && t.closest('a');
      // 2) Vditor IR-mode renders `[txt](url)` as:
      //      <span data-type="a">
      //        <span class="vditor-ir__marker--bracket">[</span>
      //        <span class="vditor-ir__link">txt</span>
      //        <span class="vditor-ir__marker--bracket">]</span>
      //        <span class="vditor-ir__marker--paren">(</span>
      //        <span class="vditor-ir__marker--link">url</span>
      //        <span class="vditor-ir__marker--paren">)</span>
      //      </span>
      // The actual URL lives in `.vditor-ir__marker--link`. Vditor's own
      // click handler on the editor element finds the `[data-type="a"]`
      // ancestor and calls `window.open(markerLink.textContent)`. We need
      // to short-circuit that BEFORE it fires (capture phase) so the URL
      // never reaches the webview's nav layer.
      var dataA = t.closest && t.closest('[data-type="a"]');
      var markerLink = dataA && dataA.querySelector(':scope > .vditor-ir__marker--link');
      var url = '';
      if (a) {
        url = a.getAttribute('href') || a.href || '';
      } else if (markerLink) {
        url = (markerLink.textContent || '').trim();
      }
      if (!a && !dataA) return; // not a link click — let it through
      var isHttp = /^https?:/i.test(url);
      if (!url || isHttp) return; // external links: leave default behavior
      // Non-http link click — block all downstream handlers so the webview
      // never tries to navigate to the resolved directory.
      e.preventDefault();
      e.stopImmediatePropagation();
      e.stopPropagation();
      // Extract fragment for intra-doc scroll.
      var frag = null;
      if (url.charAt(0) === '#') frag = url.slice(1);
      else {
        try {
          var u = new URL(url, location.href);
          if (u.hash) frag = u.hash.slice(1);
        } catch(_){}
      }
      if (frag) {
        window.__zaaackGotoAnchor && window.__zaaackGotoAnchor(frag);
      }
    }
    // Register in capture phase on window/document/documentElement so we
    // fire before vditor's own bubble-phase listener on the editor element.
    window.addEventListener('click', clickHandler, true);
    document.addEventListener('click', clickHandler, true);
    document.documentElement.addEventListener('click', clickHandler, true);

    // ---- Cmd+F find-in-page overlay ----
    var bar = null, hits = [], idx = -1, lastQ = '';

    function clearHits(){
      var parents = new Set();
      hits.forEach(function(s){
        if (s.parentNode) {
          parents.add(s.parentNode);
          s.parentNode.replaceChild(document.createTextNode(s.textContent), s);
        }
      });
      parents.forEach(function(p){ try { p.normalize(); } catch(_) {} });
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
  } catch(err) { console.error('[zaaack-patch]', err); }
};
'''

CLOSE = 'vscode.postMessage({command:"ready"});})();'


def patch_one(path):
    print('=== patching', path, '===')
    with open(path) as f:
        src = f.read()

    if P1_NEW in src:
        print('[1/4] outline already enabled')
    else:
        assert src.count(P1_OLD) == 1, 'P1 anchor not found or not unique'
        src = src.replace(P1_OLD, P1_NEW, 1)
        print('[1/4] outline option inserted')

    if P2_NEW in src:
        print('[2/4] after() hook already installed')
    else:
        assert src.count(P2_OLD) == 1, 'P2 anchor not found or not unique'
        src = src.replace(P2_OLD, P2_NEW, 1)
        print('[2/4] after() hook installed')

    # P4: postMessage wrap. Idempotent: re-inject by stripping old wrap block.
    if P4_MARKER in src:
        # Strip from marker through to the trailing 'window.global=window;'
        i = src.find(P4_MARKER)
        # Walk backward to start of the marker insertion site (after acquireVsCodeApi line)
        # The reinjection target is 'acquireVsCodeApi();' followed by marker.
        # We replace from marker through 'window.global=window;' (inclusive).
        anchor_end = 'window.global=window;'
        j = src.find(anchor_end, i)
        assert j != -1, 'cannot find window.global=window; after P4 marker'
        j_end = j + len(anchor_end)
        # Drop the entire wrapped block, leaving the bare anchor needing P4_NEW.
        src = src[:i] + 'window.global=window;' + src[j_end:]
        print('[4/4] removed prior postMessage wrap block')

    if P4_OLD in src:
        assert src.count(P4_OLD) == 1, 'P4 anchor not found or not unique'
        src = src.replace(P4_OLD, P4_NEW, 1)
        print('[4/4] postMessage wrap installed')
    else:
        # Already wrapped (P4_MARKER block present without bare anchor) — skip.
        print('[4/4] postMessage wrap already installed')

    if ENHANCE_MARKER in src:
        # Re-injecting an updated enhancer: remove old block and re-add.
        # Old block is from `/*__zaaackEnhance__*/` to the next `})();`.
        i = src.find(ENHANCE_MARKER)
        j = src.find('})();', i)
        assert j != -1, 'cannot find IIFE close after marker'
        # Remove old enhancer text but keep the trailing `})();`
        src = src[:i] + src[j:]
        print('[3/4] removed prior enhancer block')

    assert src.count(CLOSE) == 1, 'P3 anchor not found or not unique'
    src = src.replace(CLOSE,
                      'vscode.postMessage({command:"ready"});' + ENHANCE_JS + '})();',
                      1)
    print('[3/4] __zaaackEnhance defined')

    with open(path, 'w') as f:
        f.write(src)
    print('done\n')


def main():
    paths = []
    for g in CANDIDATE_GLOBS:
        paths.extend(glob.glob(os.path.expanduser(g)))
    if not paths:
        print('No zaaack main.js found in any extensions dir', file=sys.stderr)
        sys.exit(1)
    print('Targets:')
    for p in paths:
        print(' -', p)
    print()
    for p in paths:
        patch_one(p)


if __name__ == '__main__':
    main()
