#!/usr/bin/env python3
"""Patch zaaack markdown-editor to add: VS Code sidebar outline (TreeView),
intra-doc anchor nav, and Cmd+F find-in-page. Idempotent: re-running is safe.

Patches main.js, extension.js, and package.json under every installed copy
in both ~/.vscode/extensions and ~/.cursor/extensions.
After running, reload each affected IDE window (Developer: Reload Window).
"""
import os, sys, glob, shutil, time

ROOT_GLOBS = [
    os.path.expanduser('~/.vscode/extensions/zaaack.markdown-editor-*/'),
    os.path.expanduser('~/.cursor/extensions/zaaack.markdown-editor-*/'),
]


def backup(path):
    bak = f"{path}.bak.{int(time.time())}"
    shutil.copy2(path, bak)
    return bak


def strip_block(src, start_marker, end_marker):
    """Remove text from start_marker through end_marker (inclusive), plus
    leading indentation on the marker line and trailing newline."""
    i = src.find(start_marker)
    if i == -1:
        return src, False
    j = src.find(end_marker, i)
    assert j != -1, f'Found {start_marker} but no matching {end_marker}'
    j += len(end_marker)
    # Eat trailing newline
    if j < len(src) and src[j] == '\n':
        j += 1
    # Eat leading whitespace on the marker's line back to the preceding \n
    k = i
    while k > 0 and src[k - 1] in ' \t':
        k -= 1
    if k > 0 and src[k - 1] == '\n':
        i = k  # keep the preceding \n (it terminates the previous line)
    return src[:i] + src[j:], True


# ====================================================================
# main.js patches
# ====================================================================

# Patch 1 REMOVAL: undo vditor built-in outline (now using VS Code TreeView)
P1_PATCHED = 'toolbarConfig:{pin:!0},outline:{enable:!0,position:"left"},'
P1_ORIGINAL = 'toolbarConfig:{pin:!0},'

# Patch 2: hook after() to call our enhancer
P2_OLD = 'after(){V_(),Y_(),sB(),K_()}'
P2_NEW = 'after(){V_(),Y_(),sB(),K_(),window.__zaaackEnhance&&window.__zaaackEnhance()}'

# Patch 4: wrap vscode.postMessage to drop intra-doc open-link messages
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

# Patch 3: enhancer — anchor nav + find-in-page + scroll-to-heading listener
# (vditor outline + resizer REMOVED; scroll-to-heading for VS Code TreeView ADDED)
ENHANCE_MARKER = '/*__zaaackEnhance__*/'
ENHANCE_END_MARKER = '/*__zaaackEnhance_end__*/'
ENHANCE_JS = ENHANCE_MARKER + r'''
// Heading lookup + scroll helper, exposed globally so the postMessage wrap
// and the VS Code sidebar outline TreeView can use it.
function slugify(s){
  return decodeURIComponent(s||'')
    .trim().toLowerCase()
    .replace(/^[#*\-_\s]+/,'')
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
  var ed = document.querySelector('.vditor-ir__content')
        || document.querySelector('.vditor-ir')
        || document.querySelector('.vditor-reset')
        || document.querySelector('#app')
        || document.body;
  if (!ed) return false;
  var t = null;
  try { t = ed.querySelector('[id="' + (window.CSS && CSS.escape ? CSS.escape(frag) : frag) + '"]'); } catch(_){}
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

    // ---- Fix: outline "More" menu item invisible ----
    (function injectCssFixes(){
      if (document.getElementById('__zk-css-fixes')) return;
      var s = document.createElement('style');
      s.id = '__zk-css-fixes';
      s.textContent = [
        'body[data-use-vscode-theme-color="1"] .vditor{',
        '  --toolbar-icon-hover-color:var(--vscode-textLink-foreground,var(--vscode-editor-foreground));',
        '}',
      ].join('');
      document.head.appendChild(s);
    })();

    // ---- Intra-doc anchor link navigation ----
    function clickHandler(e){
      var t = e.target;
      if (!t) return;
      var a = t.closest && t.closest('a');
      var dataA = t.closest && t.closest('[data-type="a"]');
      var markerLink = dataA && dataA.querySelector(':scope > .vditor-ir__marker--link');
      var url = '';
      if (a) {
        url = a.getAttribute('href') || a.href || '';
      } else if (markerLink) {
        url = (markerLink.textContent || '').trim();
      }
      if (!a && !dataA) return;
      var isHttp = /^https?:/i.test(url);
      if (!url || isHttp) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      e.stopPropagation();
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
        + '<button id="__zk-prev" title="Previous (Shift+Enter)" style="cursor:pointer;background:transparent;color:inherit;border:1px solid var(--vscode-widget-border,#454545);padding:1px 7px;font:inherit;">&#x2191;</button>'
        + '<button id="__zk-next" title="Next (Enter)" style="cursor:pointer;background:transparent;color:inherit;border:1px solid var(--vscode-widget-border,#454545);padding:1px 7px;font:inherit;">&#x2193;</button>'
        + '<button id="__zk-close" title="Close (Esc)" style="cursor:pointer;background:transparent;color:inherit;border:1px solid var(--vscode-widget-border,#454545);padding:1px 7px;font:inherit;">&#xd7;</button>';
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

    // ---- Listen for scroll-to-heading from extension (VS Code sidebar outline) ----
    window.addEventListener('message', function(e) {
      var d = e.data;
      if (d && d.command === 'scroll-to-heading' && d.slug) {
        window.__zaaackGotoAnchor && window.__zaaackGotoAnchor(d.slug);
      }
    });

  } catch(err) { console.error('[zaaack-patch]', err); }
};
''' + ENHANCE_END_MARKER

CLOSE = 'vscode.postMessage({command:"ready"});})();'


def patch_main_js(path):
    print(f'  main.js: {path}')
    with open(path) as f:
        src = f.read()

    # P1 removal: undo vditor built-in outline (now using VS Code sidebar)
    if P1_PATCHED in src:
        src = src.replace(P1_PATCHED, P1_ORIGINAL, 1)
        print('    [1/4] vditor outline removed (now using VS Code sidebar)')
    else:
        print('    [1/4] vditor outline already absent')

    # P2: after() hook
    if P2_NEW in src:
        print('    [2/4] after() hook already installed')
    else:
        assert src.count(P2_OLD) == 1, 'P2 anchor not found or not unique'
        src = src.replace(P2_OLD, P2_NEW, 1)
        print('    [2/4] after() hook installed')

    # P4: postMessage wrap (strip old, re-inject)
    if P4_MARKER in src:
        i = src.find(P4_MARKER)
        anchor_end = 'window.global=window;'
        j = src.find(anchor_end, i)
        assert j != -1, 'cannot find window.global=window; after P4 marker'
        j_end = j + len(anchor_end)
        src = src[:i] + 'window.global=window;' + src[j_end:]
        print('    [4/4] removed prior postMessage wrap')

    if P4_OLD in src:
        assert src.count(P4_OLD) == 1, 'P4 anchor not found or not unique'
        src = src.replace(P4_OLD, P4_NEW, 1)
        print('    [4/4] postMessage wrap installed')
    else:
        print('    [4/4] postMessage wrap already installed')

    # P3: enhancer (strip old, re-inject)
    if ENHANCE_MARKER in src:
        i = src.find(ENHANCE_MARKER)
        # Use end marker if present; fall back to scanning for IIFE close
        if ENHANCE_END_MARKER in src:
            j = src.find(ENHANCE_END_MARKER, i)
            assert j != -1
            j += len(ENHANCE_END_MARKER)
        else:
            # Legacy enhancer without end marker: find the IIFE close.
            # Must skip past internal })(); patterns (e.g. injectCssFixes IIFE).
            # The file's IIFE close is the LAST })(); in the file.
            j = src.rfind('})();')
            assert j != -1, 'cannot find IIFE close'
        src = src[:i] + src[j:]
        print('    [3/4] removed prior enhancer')

    assert src.count(CLOSE) == 1, 'P3 anchor not found or not unique'
    src = src.replace(CLOSE,
                      'vscode.postMessage({command:"ready"});' + ENHANCE_JS + '})();',
                      1)
    print('    [3/4] enhancer installed')

    with open(path, 'w') as f:
        f.write(src)


# ====================================================================
# extension.js patches — VS Code sidebar outline TreeView
# ====================================================================

# Marker pairs for stripping on re-run
EXT_MARKERS = [
    ('/*__zk_outline__*/',            '/*__zk_outline_end__*/'),
    ('/*__zk_outline_activate__*/',   '/*__zk_outline_activate_end__*/'),
    ('/*__zk_outline_viewstate__*/',  '/*__zk_outline_viewstate_end__*/'),
    ('/*__zk_outline_docchange__*/',  '/*__zk_outline_docchange_end__*/'),
    ('/*__zk_outline_dispose__*/',    '/*__zk_outline_dispose_end__*/'),
    ('/*__zk_outline_create__*/',     '/*__zk_outline_create_end__*/'),
]

# E_CLASS: MarkdownOutlineProvider + helpers, inserted before `class EditorPanel {`
EXT_CLASS = '''\
/*__zk_outline__*/
function _zkSlugify(s) {
    return (s || '').trim().toLowerCase()
        .replace(/^[#*\\-_\\s]+/, '')
        .replace(/\\s+/g, '-')
        .replace(/[^\\w\\-]/g, '');
}
class _ZkHeading {
    constructor(label, level, line, slug) {
        this.label = label;
        this.level = level;
        this.line = line;
        this.slug = slug;
        this.children = [];
    }
}
class MarkdownOutlineProvider {
    constructor() {
        this._onDidChange = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChange.event;
        this._roots = [];
    }
    refresh(doc) {
        this._roots = doc ? this._buildTree(this._parse(doc.getText())) : [];
        this._onDidChange.fire();
    }
    _parse(text) {
        const result = [];
        const lines = text.split('\\n');
        let inCodeBlock = false;
        let inFrontmatter = false;
        for (let i = 0; i < lines.length; i++) {
            if (i === 0 && lines[0].trim() === '---') { inFrontmatter = true; continue; }
            if (inFrontmatter) { if (lines[i].trim() === '---') inFrontmatter = false; continue; }
            if (/^(`{3,}|~{3,})/.test(lines[i])) { inCodeBlock = !inCodeBlock; continue; }
            if (inCodeBlock) continue;
            const m = lines[i].match(/^(#{1,6})\\s+(.+)/);
            if (m) {
                const level = m[1].length;
                const label = m[2].replace(/\\s*#+\\s*$/, '').trim();
                const slug = _zkSlugify(label);
                result.push({ label, level, line: i, slug });
            }
        }
        return result;
    }
    _buildTree(headings) {
        const roots = [];
        const stack = [];
        for (const h of headings) {
            const node = new _ZkHeading(h.label, h.level, h.line, h.slug);
            while (stack.length > 0 && stack[stack.length - 1].level >= h.level) stack.pop();
            if (stack.length === 0) roots.push(node);
            else stack[stack.length - 1].children.push(node);
            stack.push(node);
        }
        return roots;
    }
    getTreeItem(el) {
        const item = new vscode.TreeItem(
            el.label,
            el.children.length > 0
                ? vscode.TreeItemCollapsibleState.Expanded
                : vscode.TreeItemCollapsibleState.None
        );
        item.command = { command: 'markdownEditorOutline.scrollTo', title: '', arguments: [el.slug] };
        item.tooltip = '#'.repeat(el.level) + ' ' + el.label;
        return item;
    }
    getChildren(el) {
        return el ? el.children : this._roots;
    }
}
/*__zk_outline_end__*/
'''

# E_ACTIVATE: tree view registration inside activate()
EXT_ACTIVATE = '''
    /*__zk_outline_activate__*/
    // Clear stale vditor outline preference (outline now lives in VS Code sidebar).
    // Previous patch injected outline:{enable:true} into vditor config; vditor saved
    // that to globalState via 'save-options'. Without this cleanup the vditor outline
    // reappears from saved state even after the config injection is removed.
    const _zkStored = context.globalState.get('vditor.options');
    if (_zkStored && _zkStored.outline && _zkStored.outline.enable) {
        _zkStored.outline = { enable: false };
        context.globalState.update('vditor.options', _zkStored);
    }
    const _zkOutline = new MarkdownOutlineProvider();
    EditorPanel._outlineProvider = _zkOutline;
    vscode.window.createTreeView('markdownEditorOutline', {
        treeDataProvider: _zkOutline,
        showCollapseAll: true,
    });
    context.subscriptions.push(
        vscode.commands.registerCommand('markdownEditorOutline.scrollTo', (slug) => {
            for (const p of EditorPanel.panelsByPath.values()) {
                if (p._panel.active) {
                    p._panel.webview.postMessage({ command: 'scroll-to-heading', slug });
                    break;
                }
            }
        })
    );
    /*__zk_outline_activate_end__*/'''

# E_VIEWSTATE: track panel focus to show/hide outline
EXT_VIEWSTATE = '''
        /*__zk_outline_viewstate__*/
        this._panel.onDidChangeViewState((e) => {
            if (e.webviewPanel.active) {
                vscode.commands.executeCommand('setContext', 'markdownEditorActive', true);
                if (EditorPanel._outlineProvider) EditorPanel._outlineProvider.refresh(this._document);
            } else {
                setTimeout(() => {
                    let any = false;
                    for (const p of EditorPanel.panelsByPath.values()) {
                        if (p._panel.active) { any = true; break; }
                    }
                    if (!any) {
                        vscode.commands.executeCommand('setContext', 'markdownEditorActive', false);
                        if (EditorPanel._outlineProvider) EditorPanel._outlineProvider.refresh(null);
                    }
                }, 50);
            }
        }, null, this._disposables);
        /*__zk_outline_viewstate_end__*/'''

# E_DOCCHANGE: refresh outline on document changes (even when webview is active)
EXT_DOCCHANGE = '''\
            /*__zk_outline_docchange__*/
            if (EditorPanel._outlineProvider && this._panel.active) {
                clearTimeout(EditorPanel._outlineRefreshTimer);
                EditorPanel._outlineRefreshTimer = setTimeout(() => {
                    EditorPanel._outlineProvider.refresh(this._document);
                }, 500);
            }
            /*__zk_outline_docchange_end__*/
'''

# E_DISPOSE: clear outline when last panel closes
EXT_DISPOSE = '''
        /*__zk_outline_dispose__*/
        if (EditorPanel.panelsByPath.size === 0) {
            vscode.commands.executeCommand('setContext', 'markdownEditorActive', false);
            if (EditorPanel._outlineProvider) EditorPanel._outlineProvider.refresh(null);
        }
        /*__zk_outline_dispose_end__*/'''

# E_CREATE: populate outline immediately when a panel opens
EXT_CREATE = '''
        /*__zk_outline_create__*/
        vscode.commands.executeCommand('setContext', 'markdownEditorActive', true);
        if (EditorPanel._outlineProvider) EditorPanel._outlineProvider.refresh(doc);
        /*__zk_outline_create_end__*/'''

# Anchors in extension.js (must match the PATCHED file with multi-file editor + theme patches)
EA_CLASS     = 'class EditorPanel {'
EA_ACTIVATE  = "context.globalState.setKeysForSync([KeyVditorOptions]);"
EA_VIEWSTATE = "this._init();"
EA_DOCCHANGE = "            // don't change webview panel when webview panel is focus"
EA_DISPOSE   = "EditorPanel.panelsByPath.delete(this._fsPath);"
EA_CREATE    = "EditorPanel.panelsByPath.set(fsPath, newPanel);"


def patch_extension_js(path):
    print(f'  extension.js: {path}')
    with open(path) as f:
        src = f.read()

    # Safety check: multi-file editor patch must be present
    if 'EditorPanel.panelsByPath' not in src:
        print('    WARNING: multi-file editor patch not found — skipping outline patches')
        print('    (Apply the panelsByPath patch to extension.js first)')
        return

    # Strip any existing outline blocks (idempotent re-injection)
    stripped_any = False
    for start_m, end_m in EXT_MARKERS:
        src, did = strip_block(src, start_m, end_m)
        stripped_any = stripped_any or did
    if stripped_any:
        print('    stripped prior outline patches')

    # E_CLASS: insert before class EditorPanel
    assert src.count(EA_CLASS) == 1, f'anchor not found or not unique: {EA_CLASS}'
    src = src.replace(EA_CLASS, EXT_CLASS + EA_CLASS, 1)
    print('    [E1] MarkdownOutlineProvider class inserted')

    # E_ACTIVATE: insert after setKeysForSync
    assert src.count(EA_ACTIVATE) == 1, f'anchor not found or not unique: {EA_ACTIVATE}'
    src = src.replace(EA_ACTIVATE, EA_ACTIVATE + EXT_ACTIVATE, 1)
    print('    [E2] TreeView registration inserted in activate()')

    # E_VIEWSTATE: insert after this._init()
    assert src.count(EA_VIEWSTATE) == 1, f'anchor not found or not unique: {EA_VIEWSTATE}'
    src = src.replace(EA_VIEWSTATE, EA_VIEWSTATE + EXT_VIEWSTATE, 1)
    print('    [E3] onDidChangeViewState handler inserted')

    # E_DOCCHANGE: insert before the "don't change webview" comment
    assert src.count(EA_DOCCHANGE) == 1, f'anchor not found or not unique: {EA_DOCCHANGE}'
    src = src.replace(EA_DOCCHANGE, EXT_DOCCHANGE + EA_DOCCHANGE, 1)
    print('    [E4] outline refresh on doc change inserted')

    # E_DISPOSE: insert after panelsByPath.delete
    assert src.count(EA_DISPOSE) == 1, f'anchor not found or not unique: {EA_DISPOSE}'
    src = src.replace(EA_DISPOSE, EA_DISPOSE + EXT_DISPOSE, 1)
    print('    [E5] dispose cleanup inserted')

    # E_CREATE: insert after panelsByPath.set
    assert src.count(EA_CREATE) == 1, f'anchor not found or not unique: {EA_CREATE}'
    src = src.replace(EA_CREATE, EA_CREATE + EXT_CREATE, 1)
    print('    [E6] initial outline refresh inserted in createOrShow()')

    with open(path, 'w') as f:
        f.write(src)


# ====================================================================
# package.json patches — declare the TreeView + activation event
# ====================================================================

PKG_MARKER = '"markdownEditorOutline"'

# Add activation event for the outline view
PKG_AE_OLD = '"onLanguage:markdown"\n\t],'
PKG_AE_NEW = '"onLanguage:markdown",\n\t\t"onView:markdownEditorOutline"\n\t],'

# Add views contribution (insert between keybindings close and contributes close)
PKG_VIEWS_OLD = '\t\t]\n\t},\n\t"scripts": {'
PKG_VIEWS_NEW = (
    '\t\t],\n'
    '\t\t"views": {\n'
    '\t\t\t"explorer": [\n'
    '\t\t\t\t{\n'
    '\t\t\t\t\t"id": "markdownEditorOutline",\n'
    '\t\t\t\t\t"name": "Markdown Outline",\n'
    '\t\t\t\t\t"when": "markdownEditorActive"\n'
    '\t\t\t\t}\n'
    '\t\t\t]\n'
    '\t\t}\n'
    '\t},\n'
    '\t"scripts": {'
)


def patch_package_json(path):
    print(f'  package.json: {path}')
    with open(path) as f:
        src = f.read()

    if PKG_MARKER in src:
        print('    outline view already declared')
        return

    # Add activationEvent
    assert src.count(PKG_AE_OLD) == 1, f'activationEvents anchor not found:\n  {PKG_AE_OLD!r}'
    src = src.replace(PKG_AE_OLD, PKG_AE_NEW, 1)
    print('    activationEvent added')

    # Add views declaration
    assert src.count(PKG_VIEWS_OLD) == 1, f'contributes views anchor not found:\n  {PKG_VIEWS_OLD!r}'
    src = src.replace(PKG_VIEWS_OLD, PKG_VIEWS_NEW, 1)
    print('    views declaration added')

    with open(path, 'w') as f:
        f.write(src)


# ====================================================================
# main
# ====================================================================

def main():
    roots = []
    for g in ROOT_GLOBS:
        roots.extend(sorted(glob.glob(g)))
    if not roots:
        print('No zaaack extension found in any extensions dir', file=sys.stderr)
        sys.exit(1)

    print(f'Found {len(roots)} extension(s):')
    for r in roots:
        print(f'  {r}')
    print()

    for root in roots:
        print(f'=== {root} ===')
        main_js  = os.path.join(root, 'media', 'dist', 'main.js')
        ext_js   = os.path.join(root, 'out', 'extension.js')
        pkg_json = os.path.join(root, 'package.json')

        # Backup all files before patching
        for f in [main_js, ext_js, pkg_json]:
            if os.path.exists(f):
                backup(f)

        if os.path.exists(main_js):
            patch_main_js(main_js)
        else:
            print(f'  main.js: NOT FOUND at {main_js}')

        if os.path.exists(ext_js):
            patch_extension_js(ext_js)
        else:
            print(f'  extension.js: NOT FOUND at {ext_js}')

        if os.path.exists(pkg_json):
            patch_package_json(pkg_json)
        else:
            print(f'  package.json: NOT FOUND at {pkg_json}')

        print()

    print('Done. Reload each IDE window (Developer: Reload Window).')
    print('Verify: node -c <extension-root>/media/dist/main.js')
    print('Verify: node -c <extension-root>/out/extension.js')


if __name__ == '__main__':
    main()
