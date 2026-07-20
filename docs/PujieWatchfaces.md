# Pujie watchfaces

## Search summary

Searched `~/src` first, then expanded across all of `$HOME`.

- No file name or file content match for the literal string `infovore` was found in the JS sources.
- The name **Infovore** does appear in personal notes/logs, which tie that watchface to the Pujie JS files below.

## Located JS files and backups

### `~/src/PujieUtils.js`

Main custom Pujie helper script currently found in home.

What it contains:

- Pujie meta-variable date/time shim via `[year]`, `[month_n]`, `[day_n]`, `[h24]`, `[m]`, `[s]`, `[ms]`, `[gmt_offset]`
- home location constants: `37.3813, -122.1447`
- distance and bearing to a target
- cached solar-system hour-angle table for Moon, Mercury, Venus, Mars, Jupiter, Saturn
- sunrise/sunset calculation
- exported values:
  - `PujieUtils.SolarSystem.Sunrise`
  - `PujieUtils.SolarSystem.Sunset`
  - `PujieUtils.SolarSystem.DawnHourAngle`
  - `PujieUtils.SolarSystem.DuskHourAngle`

### `~/src/PujieUtils.js.bak`

Backup of `PujieUtils.js`.

Observed differences vs current `PujieUtils.js`:

- older comments/debug remnants inside `hourAngleOf`
- older dawn/dusk representation:
  - `DawnHourAngle = 12 - (Sun_dayLength/2)`
  - `DuskHourAngle = 12 + (Sun_dayLength/2)`
- current file instead stores sunrise/sunset and uses:
  - `DawnHourAngle = 24 - (Sun_dayLength/2)`
  - `DuskHourAngle = Sun_dayLength/2`

### `~/src/PujieUtils20231125.js`

Dated snapshot from `2023.11.25`.

Characteristics:

- alternate implementation style using `global`
- appears to be an experiment/prototype around astronomy calculations
- likely related to the later cached hour-angle work mentioned in logs on `2023.11.30`

### `~/src/DeathClock.js`

Custom Pujie text automation script for **heartbeats until death**.

Current script:

- uses Pujie meta-variables
- counts heartbeats until `2052.03.30`
- returns a rounded string result for display

### `~/src/DeathClock.js~`

Backup/older draft of `DeathClock.js`.

Observed differences vs current `DeathClock.js`:

- older rough draft used modern JS (`const`, `let`)
- printed to console instead of returning a display string
- had a likely typo/bug: `h24l`
- did not yet adapt cleanly to Pujie meta-variables

## Related development source

### `~/src/PujieUtils/src/astronomy_lite.js`
### `~/src/PujieUtils/dist/astronomy_lite.js`

Standalone astronomy workbench/package.

Evidence:

- package exists at `~/src/PujieUtils/`
- package name: `pujieutils`
- files include `HourAngle`
- they hard-code the same home coordinates used in the watchface JS

This looks like the source/prototyping area behind the later watchface-friendly cached calculations.

## Notes that identify the watchface as "Infovore"

### `~/My Drive/HoltzBot/FamilyLogs.md`
### `~/My Drive/HoltzBot/Log Family.txt`

Timeline entries:

- `2023.11.12` — "BH starts creating Puji watchface."
- `2023.11.14` — `BH "Infovore" watchface: death clock, home bearing, unix time, etc.`
- `2023.11.30` — `BH implements cached solar system hour angle calculation for Pujie WearOS watchface.`
- `2023.12.05` — `BH adds to Infovore Pujie watchface: sun/moon/planets, sunrise/set times+horizons`

These line up well with:

- `DeathClock.js` for the death-clock feature
- `PujieUtils.js` for home bearing, Unix-time/date plumbing, and later astronomy additions

### `~/My Drive/Journal.txt`

Feature list for **Infovore**:

- distance and direction to home
- altitude and latest city
- lat/long and Unix time
- date and time
- rain, wind, temps low/high/current
- steps, heart rate low/high/current
- heartbeats until death (`2052.03.30` U.S. solar eclipse)
- battery % for watch and phone

Not all of these features were found in the recovered JS backups, so some watchface logic may live in:

- Pujie designer configuration rather than standalone JS
- other unrecovered snippets
- Automate/Complication text expressions

## Attached screenshot clue (`2026.07.19`)

The screenshot shows a Pujie **Automate text** expression that appears to implement or display Unix time:

```js
var secondsSinceEpoch =
  computeSecondsSinceEpoch([year], [month_n], [day_n], [h24], [m], [s], [gmt_offset]);
return [com_evnt] == "No event"
  ? secondsSinceEpoch.toLocaleString()
  : [com_evnt];
```

The visible helper function starts with non-leap-year month lengths, so this looks like a custom seconds-since-epoch formatter inside Pujie text automation.

This screenshot matches the `2023.11.14` note that Infovore included **Unix time**.

## Other related artifact

### `~/My Drive/Pujie Watch Face Baseline Features V2.gdoc`

Google Drive shortcut/stub only. Current contents expose:

- Google doc id: `1XHfhAW6AmrtjNeoZc95N8S00Rylz_Jpwf8C57EkDvnw`
- owner email: `brianholtz1965@gmail.com`

Probable URL:

<https://docs.google.com/document/d/1XHfhAW6AmrtjNeoZc95N8S00Rylz_Jpwf8C57EkDvnw/edit>

## Current best reconstruction

The most likely recovered implementation split is:

1. **Infovore base watchface concept** — documented in notes on `2023.11.14`
2. **Death-clock display JS** — `~/src/DeathClock.js` with `~/src/DeathClock.js~` as backup
3. **Home bearing / date plumbing / astronomy additions** — `~/src/PujieUtils.js` with `~/src/PujieUtils.js.bak` as backup
4. **Astronomy prototype/source workspace** — `~/src/PujieUtils20231125.js` and `~/src/PujieUtils/`

## Known gaps

- No recovered file literally named `Infovore`
- No recovered JS yet for:
  - altitude/latest city
  - weather
  - steps/heart-rate
  - watch/phone battery
- Those features may have lived in watchface configuration, data providers, or separate text expressions not yet recovered
