# Voltas Lead Audit — Feedback Changes (March 18, 2026)

## Source
Feedback from: https://docs.google.com/document/d/10FuQxo0a4XEqI0t0E90WGaxKOHvnQgn4kybqH8baVAo/edit?tab=t.0

## 3 Corrections Applied to `build.py`

### 1. Product Count: "200+" → "74"
- **Reason**: `/collections/all` on voltas.com shows only 74 products, not 200+
- **Files changed**: `build.py` lines 42-47 (proxy signals), line 111 (platform notes)
- **Variables affected**: `{{PROXY_PRODUCT_COUNT}}`, `{{PROXY_TIER_NARRATIVE}}`, `{{PLATFORM_NOTES}}`

### 2. Instagram: "N/A (Tata Group brand — offline-heavy)" → "82.1K (@myvoltas)"
- **Reason**: Instagram account exists at https://www.instagram.com/myvoltas/ with 82.1K followers
- **Files changed**: `build.py` line 49 (proxy signal), line 46 (narrative)
- **Variables affected**: `{{PROXY_INSTAGRAM}}`, `{{PROXY_TIER_NARRATIVE}}`

### 3. Reviews: Updated to reflect Judge.me not on all templates
- **Reason**: Judge.me is installed but reviews feature not added on all product page templates
- **Files changed**: `build.py` line 48 (proxy signal), line 46 (narrative), line 273 (finding card observation), line 147 (app stack narrative), line 580 (app benchmark tag)
- **Variables affected**: `{{PROXY_REVIEW_COUNT}}`, `{{PROXY_TIER_NARRATIVE}}`, `{{APP_STACK_NARRATIVE}}`, finding card observations, app HTML

## Specific Line Changes in build.py

```python
# BEFORE → AFTER

# Line 47: Product count
"{{PROXY_PRODUCT_COUNT}}": "200+"
→ "{{PROXY_PRODUCT_COUNT}}": "74"

# Line 48: Review count
"{{PROXY_REVIEW_COUNT}}": "Limited (Judge.me recently installed)"
→ "{{PROXY_REVIEW_COUNT}}": "Limited (Judge.me installed — not on all templates)"

# Line 49: Instagram
"{{PROXY_INSTAGRAM}}": "N/A (Tata Group brand — offline-heavy)"
→ "{{PROXY_INSTAGRAM}}": "82.1K (@myvoltas)"

# Line 46: Tier narrative (full replacement)
# Old: "...With 200+ products listed, Judge.me reviews recently installed, and a strong social presence (~500K Instagram followers)..."
# New: "...Only 74 products are listed on the store (/collections/all shows 74), Judge.me reviews are recently installed but not yet added to all product page templates, and the brand maintains an active Instagram presence (82.1K followers @myvoltas)..."

# Line 111: Platform notes
# Old: "...with 200+ SKUs across ACs..."
# New: "...with 74 listed products across ACs..."

# Line 273: Finding card observation
# Old: "Judge.me reviews app is installed but reviews are not surfaced on product cards — they only appear on PDPs (if at all)"
# New: "Judge.me reviews app is installed but not added to all product page templates — reviews are not surfaced on product cards and have inconsistent visibility across PDPs"

# Line 147: App stack narrative
# Old: "Judge.me reviews appear recently installed with limited review coverage."
# New: "Judge.me reviews is installed but not added to all product page templates, resulting in inconsistent review visibility."

# Line 580: App benchmark tag HTML
# Old: "Recently installed — limited review coverage on products"
# New: "Installed but not added to all product page templates — inconsistent review visibility"
```

## 4. PageSpeed Data: CrUX field data → PSI API Lighthouse lab data (March 19, 2026)

**Reason**: Original scores used CrUX field data (real user metrics) instead of Lighthouse lab data (standardized test). This is a known error pattern documented in `_cro_audit_system/_feedback/common_mistakes.md`. Lab data is the standard for audit reports because it's reproducible and represents worst-case first-visit experience.

**Data source**: PageSpeed Insights web UI at pagespeed.web.dev (PSI API quota was exhausted)

**Changes**:
- Mobile PageSpeed score: 68 → **6** (was CrUX field, now Lighthouse lab)
- Desktop PageSpeed score: 54 → **18**
- LCP: 1.7s → **18.9s** | FCP: 0.7s → **8.3s** | TBT: 60ms → **2,220ms** | CLS: 0.633 → **0.477**
- CWV pass count: 3 of 5 → **0 of 5** (all fail)
- Score class: moderate → **poor** | CWV summary: warning → **mostly-fail**
- INP: N/A → **298ms** (CrUX field data available now)

**PDP data added** (new — not in original):
- Mobile: Score **21**, LCP 28.4s, FCP 5.8s, TBT 3,630ms, CLS 0.127, SI 25.2s
- Desktop: Score **37**, LCP 4.5s, FCP 1.0s, TBT 1,490ms, CLS 0.06, SI 11.5s

**Competition table corrected** (all were using incorrect data):

| Brand | Old Mobile | New Mobile | Old Desktop | New Desktop |
|-------|-----------|------------|-------------|-------------|
| Voltas | 68 | **6** | 54 | **18** |
| Blue Star | 77 | **32** | 88 | **49** |
| Havells | 86 | **36** | 91 | **28** |
| Crompton | 96 | **30** | 98 | **56** |
| Daikin | 52 | **53** | 65 | **78** |

**Variables affected**: `{{PS_CLIENT_MOBILE_SCORE}}`, `{{PS_CLIENT_MOBILE_CLASS}}`, `{{PS_CLIENT_MOBILE_VERDICT}}`, all `{{PS_CLIENT_*}}` CWV variables, `{{CWV_SUMMARY_CLASS}}`, `{{CWV_PASS_ICON}}`, `{{CWV_PASS_COUNT}}`, `{{PS_COMBINED_NARRATIVE}}`, `{{PS_COMPETITION_TABLE_ROWS}}`, `{{CDN_IMAGE_NOTE}}`, `{{CDN_COMPRESSION_NOTE}}`

**Narratives rewritten** to reflect critical performance state and include PDP data.

## Deployment Status
- ✅ `build.py` updated (March 19, 2026 — PSI API lab data + PDP)
- ✅ `index.html` regenerated (183,437 bytes, 3399 lines)
- ⬜ Needs push to GitHub for live update
- ✅ Live at: https://nishantpandey-growisto.github.io/lead-audit-voltas/ (password: voltas2026)
- ✅ Verified: Traffic & Conversion section shows corrected proxy signal cards

## To Regenerate index.html
```bash
cd _audit_reports/voltas-lead
python3 build.py
```
Note: `build.py` uses hardcoded path `/Users/growisto/Documents/Claude_Code/` for the template — this works on the host Mac but needs path adjustment in VM environments.
