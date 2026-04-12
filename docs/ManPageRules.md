# Man Page Typography Rules

This scheme splits the content into distinct categories for clarity and consistency.

## Typography

- Underline for filesystem variables and literals: mimics hyperlinks, suggesting navigation or location.
- Italics for variables: signals that the value is a placeholder, not a literal.
- Bold for commands: highlights the impact of the action.
- Colors
  - Command: DodgerBlue
  - Flag: DeepSkyBlue
  - Filesystem Variable: MediumSeaGreen
  - Filesystem Literal: Lime
  - Argument Variable: Orange
  - Argument Literal: DarkOrange
  - Freeform Variable: HotPink 
  - Freeform Literal: Magenta

## Command
- Anything that can be invoked by a shell.
- E.g. <span style="color:rgb(30,144,255);font-weight:bold;">mdar</span>, <span style="color:rgb(30,144,255);font-weight:bold;">ls</span>
- Color: DodgerBlue (RGB: 30, 144, 255)

## Flag
- Switches that modify command behavior but do not represent data values themselves.
- E.g. <span style="color:rgb(0,191,255);">--help</span>, <span style="color:rgb(0,191,255);">--verbose</span>
- Color: DeepSkyBlue (RGB: 0, 191, 255)

## Filesystem Variable
- A placeholder for a (part of a) filesystem path.
- E.g. <span style="color:rgb(60,179,113);text-decoration:underline;font-style:italic;">DIRECTORY</span>, <span style="color:rgb(60,179,113);text-decoration:underline;font-style:italic;">&lt;file&gt;</span>
- Color: MediumSeaGreen (RGB: 60, 179, 113)

## Filesystem Literal
- A concrete literal (part of a) filesystem path.
- E.g. <span style="color:rgb(0,255,0);text-decoration:underline;">/dev/null</span>, <span style="color:rgb(0,255,0);text-decoration:underline;">~/.config</span>
- Color: Lime (RGB: 0, 255, 0)

## Argument Variable
- A placeholder for a non-filesystem value (numbers, time, strings).
- E.g. <span style="color:rgb(255,165,0);font-style:italic;">NUMFILES</span>, <span style="color:rgb(255,165,0);font-style:italic;">duration</span>
- Color: Orange (RGB: 255, 165, 0)

## Argument Literal
- A predefined set of valid values, usually for flags.
- E.g. <span style="color:rgb(255,140,0);">yes</span>, <span style="color:rgb(255,140,0);">no</span>
- Color: DarkOrange (RGB: 255, 140, 0)

## Freeform Variable
- A placeholder for arbitrary user-generated content (names, comments, search queries).
- E.g. <span style="color:rgb(255,105,180);font-style:italic;">commit_comment</span>, <span style="color:rgb(255,105,180);font-style:italic;">project-name</span>
- Color: HotPink (RGB: 255, 105, 180)

## Freeform Literal
- Literal examples of arbitrary user-generated content (names, comments, search queries).
- E.g. <span style="color:rgb(255,0,255);">my first commit</span>, <span style="color:rgb(255,0,255);">Brian's Resume</span>
- Color: Magenta (RGB: 255, 0, 255)

## Danger
- Commands, flags, or actions that are dangerous or destructive, especially if no undo.
- E.g. <span style="color:rgb(255,0,0);font-weight:bold;">rm -rf /</span>, <span style="color:rgb(255,0,0);font-weight:bold;">--force</span>, <span style="color:rgb(255,0,0);font-weight:bold;">[DELETE]</span>
- Color: Pure Red (RGB: 255, 0, 0)

## Verbosity Example
- E.g. <span style="color:rgb(30,144,255);">-v=</span><span style="color:rgb(65,105,225);">find/mv</span> files, <span style="color:rgb(30,144,255);">-vv=</span>+debug, <span style="color:rgb(30,144,255);">-vvv=</span>+shell tracing

---

## Appendix: Color Reference & JavaScript Mappings

| Color Name | RGB | Hex | Shell Context | JavaScript Context |
|------------|-----|-----|---------------|-------------------|
| **DodgerBlue** | 30, 144, 255 | `#1E90FF` | Commands | Functions, methods, constructors |
| **DeepSkyBlue** | 0, 191, 255 | `#00BFFF` | Flags | Boolean options, config properties |
| **MediumSeaGreen** | 60, 179, 113 | `#3CB371` | Filesystem variables | Path parameters, module identifiers |
| **Lime** | 0, 255, 0 | `#00FF00` | Filesystem literals | String literals (paths, imports) |
| **Orange** | 255, 165, 0 | `#FFA500` | Argument variables | Function parameters, type placeholders |
| **DarkOrange** | 255, 140, 0 | `#FF8C00` | Argument literals | Enum values, predefined constants |
| **HotPink** | 255, 105, 180 | `#FF69B4` | Freeform variables | User-defined identifiers, variable names |
| **Magenta** | 255, 0, 255 | `#FF00FF` | Freeform literals | String/template literals (user content) |
| **Pure Red** | 255, 0, 0 | `#FF0000` | Dangerous operations | Destructive methods (delete, drop, clear) |

### JavaScript Examples

- <span style="color:rgb(30,144,255);font-weight:bold;">fetch</span><span style="color:rgb(255,105,180);">(</span><span style="color:rgb(255,165,0);font-style:italic;">url</span><span style="color:rgb(255,105,180);">,</span> <span style="color:rgb(255,105,180);">{</span> <span style="color:rgb(0,191,255);">method:</span> <span style="color:rgb(255,140,0);">'POST'</span> <span style="color:rgb(255,105,180);">}</span><span style="color:rgb(255,105,180);">)</span>
- <span style="color:rgb(30,144,255);font-weight:bold;">require</span><span style="color:rgb(255,105,180);">(</span><span style="color:rgb(0,255,0);text-decoration:underline;">'./config.js'</span><span style="color:rgb(255,105,180);">)</span>
- <span style="color:rgb(255,105,180);font-style:italic;">userName</span> <span style="color:rgb(255,105,180);">=</span> <span style="color:rgb(255,0,255);">'Alice'</span>
- <span style="color:rgb(30,144,255);font-weight:bold;">database</span><span style="color:rgb(255,105,180);">.</span><span style="color:rgb(255,0,0);font-weight:bold;">drop</span><span style="color:rgb(255,105,180);">()</span>

---

## Appendix: Screenshot Syntax Highlighting Color Palette

This section documents the color scheme observed in the provided JavaScript code screenshot.

| Color Name (Approx) | RGB (Approx) | Hex | JavaScript Construct |
|---------------------|--------------|-----|---------------------|
| **MediumPurple / Violet** | ~197, 134, 192 | `#C586C0` | Keywords (function, const, if, return) |
| **LightYellow / Khaki** | ~220, 220, 170 | `#DCDCAA` | Function declarations, identifiers |
| **LightBlue / SkyBlue** | ~156, 220, 254 | `#9CDCFE` | Parameters, local variables |
| **LightCoral / Salmon** | ~206, 145, 120 | `#CE9178` | String literals |
| **DarkSeaGreen / Sage** | ~78, 201, 176 | `#4EC9B0` | Method names, properties |
| **SlateGray** | ~106, 153, 85 | `#6A9955` | Comments |
| **WhiteSmoke** | ~212, 212, 212 | `#D4D4D4` | Operators, punctuation |

### Screenshot Palette Example

```javascript
// Update content labels based on pane logic
function updateContentLabels() {
  const paneLogic = getPaneLogic('logstrings');
  const includeLabel = document.querySelector('label[for="includeFilters"]');
  const excludeLabel = document.querySelector('label[for="excludeFilters"]');
  const includeField = document.getElementById('includeFilters');
  const excludeField = document.getElementById('excludeFilters');
  
  // Include filters
  if (includeLabel) {
    const originalText = 'content matches any of';
    if (!includeLabel.getAttribute('data-original-text')) {
      includeLabel.setAttribute('data-original-text', originalText);
    }
    
    // Only add prefix if field has value
    if (includeField && includeField.value.trim() !== '') {
      const prefix = paneLogic === 'or' ? 'OR ' : 'AND ';
      includeLabel.textContent = prefix + originalText;
    } else {
      includeLabel.textContent = originalText;
    }
  }
  
  // Exclude filters
  if (excludeLabel) {
    const originalText = "content doesn't match any of";
    if (!excludeLabel.getAttribute('data-original-text')) {
      excludeLabel.setAttribute('data-original-text', originalText);
    }
    
    // Only add prefix if field has value (always AND because it's a NOT filter)
    if (excludeField && excludeField.value.trim() !== '') {
      excludeLabel.textContent = 'AND ' + originalText;
    } else {
      excludeLabel.textContent = originalText;
    }
  }
}
```

**Color Mapping:**
- <span style="color:rgb(197,134,192);">function</span>, <span style="color:rgb(197,134,192);">const</span>, <span style="color:rgb(197,134,192);">if</span>, <span style="color:rgb(197,134,192);">return</span> → Keywords (MediumPurple)
- <span style="color:rgb(220,220,170);">updateContentLabels</span>, <span style="color:rgb(220,220,170);">getPaneLogic</span> → Function names (LightYellow)
- <span style="color:rgb(156,220,254);">paneLogic</span>, <span style="color:rgb(156,220,254);">includeLabel</span>, <span style="color:rgb(156,220,254);">prefix</span> → Variables (LightBlue)
- <span style="color:rgb(206,145,120);">'logstrings'</span>, <span style="color:rgb(206,145,120);">'label[for="includeFilters"]'</span> → Strings (LightCoral)
- <span style="color:rgb(78,201,176);">querySelector</span>, <span style="color:rgb(78,201,176);">getAttribute</span>, <span style="color:rgb(78,201,176);">textContent</span> → Methods/Properties (DarkSeaGreen)
- <span style="color:rgb(106,153,85);">// Update content labels based on pane logic</span> → Comments (SlateGray)
