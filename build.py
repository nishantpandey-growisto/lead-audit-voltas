#!/usr/bin/env python3
"""Build script: Populates lead_audit_spa_template.html for Voltas.

Data collected: March 17-19, 2026 — fresh mobile-first UX evaluation at 375×812,
PSI API lab data (March 19) for homepage + PDP, 3-dimension finding selection algorithm.
Industry: Electronics / Home Appliances
"""

import re, os

TEMPLATE = "/Users/growisto/Documents/Claude_Code/_cro_audit_system/templates/lead_audit_spa_template.html"
OUTPUT   = "/Users/growisto/Documents/Claude_Code/_audit_reports/voltas-lead/index.html"

# Read template
with open(TEMPLATE, "r") as f:
    html = f.read()

# ── Simple variable replacements ──────────────────────────
replacements = {
    "{{CLIENT_NAME}}": "Voltas",
    "{{CLIENT_URL}}": "voltas.com",
    "{{REPORT_DATE}}": "March 2026",
    "{{REPORT_PASSWORD}}": "voltas2026",
    "{{INDUSTRY_CATEGORY}}": "Electronics &amp; Home Appliances",
    "{{INDUSTRY_CATEGORY_SHORT}}": "electronics",

    # Section 01 — Audit Overview
    "{{SEVERITY_CRITICAL_COUNT}}": "5",
    "{{SEVERITY_IMPORTANT_COUNT}}": "7",
    "{{SEVERITY_OPPORTUNITY_COUNT}}": "4",
    "{{FINDING_COUNT_TOTAL}}": "16",
    "{{COMPETITOR_COUNT}}": "4",
    "{{APPS_PRESENT_COUNT}}": "14",
    "{{FINDING_COUNT_HOMEPAGE}}": "3",
    "{{FINDING_COUNT_COLLECTION}}": "4",
    "{{FINDING_COUNT_PDP}}": "5",
    "{{FINDING_COUNT_CART}}": "4",

    # Section 02 — Traffic & Conversion Context
    "{{PROXY_TIER_NAME}}": "Tier 4: Enterprise",
    "{{PROXY_TIER_SESSIONS}}": "200K+",
    "{{PROXY_TIER_NARRATIVE}}": "Voltas is India's largest AC brand by market share with an extensive offline dealer network. Only 74 products are listed on the store (/collections/all shows 74), Judge.me reviews are recently installed but not yet added to all product page templates, and the brand maintains an active Instagram presence (82.1K followers <a href=\"https://www.instagram.com/myvoltas/\" target=\"_blank\">@myvoltas</a>). The store signals <strong>Tier 4 (Enterprise)</strong> traffic levels based on brand strength. However, the online D2C channel appears to be a newer initiative — the Shopify store launched on the Impulse theme with significant features still unconfigured.",
    "{{PROXY_PRODUCT_COUNT}}": "74",
    "{{PROXY_REVIEW_COUNT}}": "Limited (Judge.me installed — not on all templates)",
    "{{PROXY_INSTAGRAM}}": "82.1K (@myvoltas)",
    "{{PROXY_APP_COUNT}}": "14",
    "{{PROXY_ESTIMATED_REVENUE}}": "500000000",

    # Funnel benchmarks (Electronics & Tech from Appendix C/D)
    "{{INDUSTRY_PDP_VIEW_RATE_P25}}": "60.4%",
    "{{INDUSTRY_PDP_VIEW_RATE}}": "89.6%",
    "{{INDUSTRY_PDP_VIEW_RATE_P75}}": "115.9%",
    "{{INDUSTRY_ATC_RATE_P25}}": "6.42%",
    "{{INDUSTRY_ATC_RATE}}": "11.95%",
    "{{INDUSTRY_ATC_RATE_P75}}": "20.27%",
    "{{INDUSTRY_CART_TO_CHECKOUT_P25}}": "22.8%",
    "{{INDUSTRY_CART_TO_CHECKOUT}}": "29.8%",
    "{{INDUSTRY_CART_TO_CHECKOUT_P75}}": "40.5%",
    "{{INDUSTRY_CHECKOUT_COMPLETION_P25}}": "12.3%",
    "{{INDUSTRY_CHECKOUT_COMPLETION}}": "20.7%",
    "{{INDUSTRY_CHECKOUT_COMPLETION_P75}}": "32.1%",
    "{{INDUSTRY_CVR_P25}}": "0.09%",
    "{{INDUSTRY_CVR_P50}}": "0.15%",
    "{{INDUSTRY_CVR_P75}}": "0.32%",
    "{{INDUSTRY_CVR_P50_RAW}}": "0.15",

    # Section 03: Performance & Speed (PSI API lab data — March 19, 2026)
    # Homepage: Mobile 6, Desktop 18 | PDP: Mobile 21, Desktop 37
    "{{PS_CLIENT_MOBILE_SCORE}}": "6",
    "{{PS_CLIENT_MOBILE_CLASS}}": "poor",
    "{{PS_CLIENT_MOBILE_VERDICT}}": "Critical — Voltas scores just 6/100 on Google PageSpeed Insights mobile (Lighthouse lab test). This is the lowest in the competitive set. LCP is 18.9s (target: 2.5s), FCP is 8.3s, TBT is 2,220ms, and Speed Index is 28.9s — all critically poor. CLS at 0.477 adds severe layout instability. The product page (PDP) scores slightly better at 21 mobile but still has LCP of 28.4s and TBT of 3,630ms. Desktop homepage scores 18, PDP desktop scores 37. The heavy third-party script load (CleverTap, FirstHive, Havas pixel, Boost Commerce, privEzi, SmartifyApps) combined with unoptimized images is crushing performance.",

    # Core Web Vitals (PSI API lab data — Homepage Mobile)
    "{{PS_CLIENT_LCP}}": "18.9s",
    "{{PS_CLIENT_LCP_CLASS}}": "poor",
    "{{PS_CLIENT_LCP_STATUS}}": "fail",
    "{{PS_CLIENT_LCP_LABEL}}": "Fail",
    "{{PS_CLIENT_FCP}}": "8.3s",
    "{{PS_CLIENT_FCP_CLASS}}": "poor",
    "{{PS_CLIENT_FCP_STATUS}}": "fail",
    "{{PS_CLIENT_FCP_LABEL}}": "Fail",
    "{{PS_CLIENT_TBT}}": "2,220ms",
    "{{PS_CLIENT_TBT_CLASS}}": "poor",
    "{{PS_CLIENT_TBT_STATUS}}": "fail",
    "{{PS_CLIENT_TBT_LABEL}}": "Fail",
    "{{PS_CLIENT_CLS}}": "0.477",
    "{{PS_CLIENT_CLS_CLASS}}": "poor",
    "{{PS_CLIENT_CLS_STATUS}}": "fail",
    "{{PS_CLIENT_CLS_LABEL}}": "Fail",
    "{{PS_CLIENT_INP}}": "298ms",
    "{{PS_CLIENT_INP_CLASS}}": "moderate",
    "{{PS_CLIENT_INP_STATUS}}": "warning",
    "{{PS_CLIENT_INP_LABEL}}": "Needs Work",

    "{{CWV_SUMMARY_CLASS}}": "mostly-fail",
    "{{CWV_PASS_ICON}}": "✗",
    "{{CWV_PASS_COUNT}}": "0",

    "{{PS_COMBINED_NARRATIVE}}": "Voltas scores just <strong>6 on mobile PageSpeed</strong> — the lowest in its competitive set. Every Core Web Vital fails: LCP at 18.9s (target: ≤2.5s), FCP at 8.3s, TBT at 2,220ms (target: ≤200ms), and CLS at 0.477 (target: ≤0.1). Speed Index is 28.9s, meaning the page feels painfully slow to load on mobile. The <strong>product page is equally poor at score 21</strong>, with LCP of 28.4s and TBT of 3,630ms — shoppers on mobile are waiting nearly half a minute before seeing product content. Desktop fares slightly better but is still poor: homepage 18, PDP 37. By comparison, Daikin leads mobile at 53, Havells at 36, Blue Star at 32, and Crompton at 30 — all significantly ahead. The root causes: heavy third-party scripts (CleverTap, FirstHive, Havas pixel, Boost Commerce, duplicate Facebook Pixels), unoptimized hero images/carousels causing layout shifts, and jQuery dependency errors. Improving mobile performance to even the 40-50 range could lift mobile conversions by 15-25% based on Google/Deloitte research.",

    # Section 05: Technology Assessment
    "{{TECH_HEALTH_CLASS}}": "warning",
    "{{TECH_HEALTH_ICON}}": "⚠",
    "{{TECH_HEALTH_SUMMARY}}": "4 of 6 technology areas are well-configured — 2 areas need attention",
    "{{TECH_PLATFORM_STATUS}}": "good",
    "{{TECH_PLATFORM_STATUS_LABEL}}": "Modern Platform",
    "{{PLATFORM}}": "Shopify",
    "{{PLATFORM_NOTES}}": "Shopify — auto-scaling, PCI-compliant, 99.99% uptime. Solid platform for a Tata Group brand entering D2C e-commerce with 74 listed products across ACs, water heaters, air coolers, and home appliances.",
    "{{TECH_THEME_STATUS}}": "good",
    "{{TECH_THEME_STATUS_LABEL}}": "Premium Theme",
    "{{THEME_NAME}}": "Impulse 7.4.0",
    "{{THEME_TYPE}}": "Premium Shopify Theme by ARCHETYPE",
    "{{THEME_VERSION_NOTE}}": "OS 2.0 compatible — Impulse is a well-regarded premium theme with strong conversion features",
    "{{THEME_FEATURE_NOTE}}": "Impulse has built-in support for sticky ATC, quick-add, and advanced filtering — but many of these features appear to be disabled or unconfigured on the Voltas store.",
    "{{TECH_CHECKOUT_STATUS}}": "warning",
    "{{TECH_CHECKOUT_STATUS_LABEL}}": "Friction Points",
    "{{CHECKOUT_TYPE}}": "Shopify Native + Pincode Gate",
    "{{CHECKOUT_GUEST_NOTE}}": "Guest checkout: Available",
    "{{CHECKOUT_EXPRESS_NOTE}}": "Express checkout: Not visible in cart — no GPay/Shop Pay buttons detected",
    "{{CHECKOUT_FRICTION_NOTE}}": "ATC is disabled until pincode check passes + mandatory policy checkbox before checkout — two friction barriers that compound to reduce conversion",
    "{{TECH_PAYMENTS_STATUS}}": "good",
    "{{TECH_PAYMENTS_STATUS_LABEL}}": "Comprehensive",
    "{{PAYMENT_GATEWAY}}": "Razorpay + Simpl",
    "{{PAYMENT_METHODS_NOTE}}": "UPI, Cards, Netbanking, Wallets via Razorpay",
    "{{PAYMENT_COD_NOTE}}": "COD: Not confirmed",
    "{{PAYMENT_BNPL_NOTE}}": "BNPL: Simpl Pay Later detected",
    "{{TECH_CDN_STATUS}}": "warning",
    "{{TECH_CDN_STATUS_LABEL}}": "CLS Issue",
    "{{CDN_PROVIDER}}": "Shopify CDN (Cloudflare)",
    "{{CDN_IMAGE_NOTE}}": "Images: Served via Shopify CDN. Homepage LCP is 18.9s (critically poor) and CLS at 0.477 — images and carousels shift layout during load. PDP LCP is even worse at 28.4s mobile",
    "{{CDN_COMPRESSION_NOTE}}": "Compression: Brotli/Gzip enabled. Heavy third-party script load: CleverTap, FirstHive, Havas pixel, Boost Commerce, privEzi, SmartifyApps — Speed Index 28.9s, TBT 2,220ms on homepage",
    "{{CDN_CACHING_NOTE}}": "Browser caching: Standard Shopify headers. Multiple ad/analytics scripts (Havas, FirstHive, CleverTap) plus duplicate Facebook Pixel IDs add overhead",
    "{{TECH_SECURITY_STATUS}}": "good",
    "{{TECH_SECURITY_STATUS_LABEL}}": "Secure",
    "{{SECURITY_SSL_STATUS}}": "SSL/TLS Active",
    "{{SECURITY_HTTPS_NOTE}}": "HTTPS: All pages secured",
    "{{SECURITY_PCI_NOTE}}": "PCI DSS: Compliant (via Shopify)",
    "{{SECURITY_COOKIE_NOTE}}": "Cookie consent: privEzi cookie consent SDK active — good compliance",
    "{{TECH_NARRATIVE}}": "Voltas runs on Shopify with the premium Impulse 7.4.0 theme by ARCHETYPE — a well-regarded premium theme with strong conversion features. However, many of Impulse's built-in capabilities (sticky ATC, quick-add, advanced filtering) appear to be disabled or unconfigured. The pincode serviceability check gates the Add to Cart button — users cannot add products without first entering a valid pincode, adding significant friction. The checkout flow adds a second friction barrier: a mandatory policy checkbox (\"I have read &amp; agree with the policies\") must be checked before the checkout button becomes active. These two gates — pincode + policy checkbox — compound to reduce conversion. The tech stack is heavy: GTM (GTM-KCPW6GW), GA4 (G-WF54WYTR46), Facebook Pixel (with duplicate Pixel ID error), Clarity, Klaviyo, CleverTap, FirstHive, Havas pixel, Boost Commerce, SmartifyApps, privEzi, and Judge.me. Active JS errors detected: <code>$ is not defined</code> (jQuery dependency missing), <code>Invalid visitorId</code> (CleverTap), <code>TypeError</code> in Boost Commerce script, and duplicate Facebook Pixel ID warning. Payment is handled via Razorpay with Simpl (BNPL) available — a comprehensive payment stack.",

    # Section 06: App Ecosystem
    "{{APPS_MISSING_COUNT}}": "5",
    "{{APPS_BENCHMARK_CONTEXT}}": "Voltas has 14 detected apps/scripts covering analytics, reviews, email, payments, and search — but is missing critical conversion-driving categories for high-AOV electronics: EMI calculator, cross-sell/upsell, and cart recovery",
    "{{APP_STACK_NARRATIVE}}": "Voltas has 14 apps spanning analytics (GTM, GA4, Clarity, Facebook Pixel, FirstHive, CleverTap, Havas), reviews (Judge.me), email (Klaviyo), payments (Razorpay, Simpl), search (Boost Commerce), wishlist (XB Wishlist), and cookie consent (privEzi). The analytics stack is comprehensive — arguably over-instrumented with both FirstHive and CleverTap providing overlapping CDP functionality, plus a Havas media pixel. However, critical revenue-driving categories are missing: no EMI/BNPL calculator on PDPs despite ₹30K–75K AOV products, no cross-sell/upsell app (cart has zero product recommendations), and no cart abandonment recovery app. Judge.me reviews is installed but not added to all product page templates, resulting in inconsistent review visibility. The duplicate Facebook Pixel ID error and jQuery dependency errors (<code>$ is not defined</code>) indicate integration issues that should be resolved.",

    # JS nav
    "{{UX_FINDING_1_SHORT_TITLE}}": "UX & Conversion Findings",
    "{{UX_FINDING_2_SHORT_TITLE}}": "Collection Page",
    "{{UX_FINDING_3_SHORT_TITLE}}": "Product Page",
}

for key, val in replacements.items():
    html = html.replace(key, val)

# ── Competition table rows (4 competitors — PSI API lab data March 19, 2026) ──
# Homepage scores
comp_rows = """<tr class="client-row">
                                <td>Voltas (Homepage)</td>
                                <td class="score-cell-poor">6</td>
                                <td class="score-cell-poor">18</td>
                                <td class="score-cell-poor">18.9s</td>
                                <td class="score-cell-poor">0.477</td>
                                <td class="score-cell-poor">2,220ms</td>
                            </tr>
                            <tr class="client-row" style="background: #fef2f2;">
                                <td>Voltas (PDP)</td>
                                <td class="score-cell-poor">21</td>
                                <td class="score-cell-poor">37</td>
                                <td class="score-cell-poor">28.4s</td>
                                <td class="score-cell-moderate">0.127</td>
                                <td class="score-cell-poor">3,630ms</td>
                            </tr>
                            <tr>
                                <td>Blue Star</td>
                                <td class="score-cell-poor">32</td>
                                <td class="score-cell-poor">49</td>
                                <td class="score-cell-poor">30.9s</td>
                                <td class="score-cell-good">0</td>
                                <td class="score-cell-poor">1,150ms</td>
                            </tr>
                            <tr>
                                <td>Havells</td>
                                <td class="score-cell-poor">36</td>
                                <td class="score-cell-poor">28</td>
                                <td class="score-cell-poor">23.0s</td>
                                <td class="score-cell-good">0.002</td>
                                <td class="score-cell-poor">780ms</td>
                            </tr>
                            <tr>
                                <td>Crompton</td>
                                <td class="score-cell-poor">30</td>
                                <td class="score-cell-moderate">56</td>
                                <td class="score-cell-poor">13.7s</td>
                                <td class="score-cell-good">0.027</td>
                                <td class="score-cell-poor">1,690ms</td>
                            </tr>
                            <tr>
                                <td>Daikin India</td>
                                <td class="score-cell-moderate">53</td>
                                <td class="score-cell-moderate">78</td>
                                <td class="score-cell-poor">16.6s</td>
                                <td class="score-cell-good">0</td>
                                <td class="score-cell-moderate">370ms</td>
                            </tr>"""
html = html.replace("{{PS_COMPETITION_TABLE_ROWS}}", comp_rows)

# ── Finding cards ─────────────────────────────────────────

def card(header, client_img, client_label, bench_img, bench_label, observations, recommendations, benchmark_tag):
    obs_li = "\n".join(f"                                                    <li>{o}</li>" for o in observations)
    rec_li = "\n".join(f"                                                    <li>{r}</li>" for r in recommendations)
    if client_img is None:
        client_html = f'''<div class="finding-screenshot-missing">
                                                    <div class="missing-icon">✗</div>
                                                    <div class="missing-text">Feature not present</div>
                                                </div>
                                                <div class="finding-screenshot-label client-label">{client_label}</div>'''
    else:
        client_html = f'''<img src="{client_img}" alt="Voltas">
                                                <div class="finding-screenshot-label client-label">{client_label}</div>'''
    return f"""<div class="finding-card">
                                    <div class="finding-card-header">
                                        {header}
                                    </div>
                                    <div class="finding-card-body">
                                        <div class="finding-screenshots">
                                            <div class="finding-screenshot">
                                                {client_html}
                                            </div>
                                            <div class="finding-screenshot">
                                                <img src="{bench_img}" alt="{bench_label}">
                                                <div class="finding-screenshot-label benchmark-label">{bench_label}</div>
                                            </div>
                                        </div>
                                        <div class="finding-analysis">
                                            <div class="finding-observations">
                                                <span class="finding-section-header observations-header">Observations</span>
                                                <ul>
{obs_li}
                                                </ul>
                                            </div>
                                            <div class="finding-recommendations">
                                                <span class="finding-section-header recommendations-header">Recommendations</span>
                                                <ul>
{rec_li}
                                                </ul>
                                                <span class="finding-benchmark-tag">{benchmark_tag}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>"""

# ═══════════════════════════════════════════════════════════
# HOMEPAGE (3 cards)
# ═══════════════════════════════════════════════════════════
hp_cards = "\n".join([
    card(
        "Trust badges and USP icons on the homepage can increase visitor confidence by 30–40% — Voltas has no trust/USP section below the hero",
        "screenshots/hp_products_client.jpeg", "Voltas — Homepage (no trust section)",
        "screenshots/crompton_pdp_colors.jpeg", "Crompton — Trust icons: Buy In Store, Warranty, Service, Top Rated",
        [
            "The Voltas homepage goes directly from the hero carousel to \"Best Sellers\" product grid — there is no trust-building section (USPs, warranty badges, Tata guarantee, delivery promises)",
            "For high-AOV appliances (₹30K–75K), trust signals are critical in the first scroll — customers need reassurance before browsing products",
            "Crompton displays clear trust icons below their product info: \"Buy In Store Or Online\", \"Service And Installation\", \"Product Warranty\", \"Top Rated Products\" — these convert browsers into buyers by reducing perceived risk",
            "Voltas's brand heritage (Tata Group, India's #1 AC brand) is completely absent from the homepage — no trust badges, no warranty icons, no service promise",
        ],
        [
            "Add a trust/USP bar below the hero with 4–5 icons: \"Tata Group Company\", \"India's #1 AC Brand\", \"Free Installation\", \"10-Year Warranty\", \"Pan-India Service Network\"",
            "Add a testimonials/awards section showcasing brand heritage and customer trust metrics",
        ],
        "Standard — 9/10 top electronics stores have trust/USP sections on homepage",
    ),
    card(
        "Rich product cards with specs, energy ratings &amp; CTAs increase click-through by 15–25% — Voltas cards show only image, name &amp; price",
        "screenshots/hp_products_client.jpeg", "Voltas — Best Sellers (minimal cards: image, model name, price only)",
        "screenshots/bluestar_product_cards.jpeg", "Blue Star — Rich cards with series name, tonnage, BEE star ratings, Compare &amp; Explore CTAs",
        [
            "Voltas Best Seller product cards show only: product image, technical model name, MRP, offer price, and savings — no energy ratings, no tonnage options, no comparison CTA, no review counts",
            "Product titles are excessively long and technical: \"VOLTAS SPLIT AIR CONDITIONER, 1.5 TON, 3 STAR - 183INV VECTRA ZEPHYR GOLD\" — this is a SKU name, not a customer-friendly title",
            "Blue Star product cards show series name, starting price, tonnage options (1 TON / 1.5 TON), BEE star rating badges, Compare button, and Explore CTA — far richer information density that helps buyers shortlist without visiting each PDP",
            "Judge.me reviews app is installed but not added to all product page templates — enabling star ratings on cards would add another layer of decision-making data",
        ],
        [
            "Enrich product cards: add BEE star rating badge, tonnage/capacity options, and a Compare CTA to match competitor card density",
            "Rewrite product titles to be customer-friendly: \"Vectra Emerald Split AC — 1 Ton, 3 Star\" instead of the full model code",
            "Enable Judge.me star ratings on collection/homepage product cards — show average rating + review count below the product title",
        ],
        "Standard — 8/10 top electronics stores show rich product cards with specs, ratings &amp; CTAs",
    ),
    card(
        "A social proof section (reviews, customer count, awards) builds purchase confidence for high-AOV products — Voltas has none",
        "screenshots/mockup_social_proof.jpeg", "Proposed Implementation — Voltas Homepage",
        "screenshots/bajaj_social_proof.jpeg", "Bajaj — \"Loved by Millions\" social proof section with star ratings and review cards",
        [
            "The homepage has no social proof section — no customer testimonials, no review carousel, no \"trusted by X customers\" counter, no awards or certifications display",
            "For ₹30K–75K purchases, buyers actively seek validation — Voltas being a Tata Group brand is a massive trust asset that is completely underleveraged on the website",
            "Bajaj prominently displays a \"Loved by Millions of Consumers\" section with star ratings and customer review cards — this type of social proof builds purchase confidence for high-AOV appliances",
        ],
        [
            "Add a \"Why Choose Voltas\" section with: Tata Group heritage, pan-India service network reach, customer satisfaction stats, and industry awards",
            "Add a review carousel pulling from Judge.me — even 10–15 genuine reviews with photos create significant social proof for appliance purchases",
        ],
        "Standard — 8/10 top electronics stores have social proof sections",
    ),
])

# ═══════════════════════════════════════════════════════════
# COLLECTION (4 cards)
# ═══════════════════════════════════════════════════════════
col_cards = "\n".join([
    card(
        "Key spec icons on collection cards help buyers compare at a glance — Voltas shows only images and model codes",
        "screenshots/col_cards_client.jpeg", "Voltas — AC Collection (no spec badges)",
        "screenshots/daikin_product_cards.jpeg", "Daikin — Product cards with Star Rating, Capacity, Technology specs + Compare",
        [
            "Voltas collection cards show: product image, full technical model name (ALL CAPS), MRP, offer price, savings, and an \"Add to compare\" link — but no structured spec badges for tonnage, star rating, or key features",
            "For AC purchases, buyers need to quickly compare: tonnage (1/1.5/2 ton), energy rating (3/4/5 star), and key feature (inverter/fixed speed) — these should be scannable badges, not buried in the title",
            "Daikin product cards display structured specs (Star Rating, Capacity, Technology, Compressor type) as scannable rows + a Compare button — making quick comparison effortless",
            "The \"Add to compare\" feature exists (good) but spec badges would reduce the need for comparison by making key differences visible at the card level",
        ],
        [
            "Add structured spec badges below each product image: tonnage pill, star rating badge, and one key feature tag (e.g., \"Inverter\", \"AI Mode\")",
            "Use Impulse theme's built-in swatch/variant display to show tonnage or color variants directly on cards",
        ],
        "Standard — 9/10 top electronics stores show spec icons on collection cards",
    ),
    card(
        "Advanced category filters with spec-based facets increase product discovery by 25–40% — Voltas has basic filter only",
        "screenshots/col_titles_client.jpeg", "Voltas — Basic Filter + Sort",
        "screenshots/daikin_filters.jpeg", "Daikin — AC Finder tool with Room Size, Space Type, Roof Condition filters",
        [
            "Voltas collection page has a simple \"Filter\" button and \"Best selling\" sort dropdown — opening the filter reveals basic options but lacks spec-based facets (tonnage, star rating, price range, features)",
            "For a catalog with 50+ AC models, spec-based filtering is essential — buyers typically know their tonnage requirement and budget range before browsing",
            "Daikin goes beyond basic filters with an interactive AC Finder tool: Room Size, Space Type, Roof Condition — guiding buyers to the right product even if they don't know the tonnage",
            "The filter UX on mobile requires a full-page overlay — no sticky filter pills or quick-filter chips visible during browsing",
        ],
        [
            "Configure Boost Commerce filters with electronics-specific facets: Tonnage (1/1.5/2 Ton), Star Rating (3/4/5 Star), Price Range (₹25K-35K, ₹35K-50K, ₹50K+), Type (Split/Window), Features (Inverter, Wi-Fi, etc.)",
            "Consider adding a guided \"AC Finder\" quiz similar to Daikin — this dramatically improves conversion for buyers who don't know specs but know their room/requirements",
        ],
        "Standard — 9/10 top electronics stores have advanced spec-based filters",
    ),
    card(
        "Excessively long product titles reduce scannability and mobile usability — Voltas titles are 60–80 characters of model codes",
        "screenshots/col_titles_client.jpeg", "Voltas — Long Technical Titles",
        "screenshots/bluestar_collection.jpeg", "Blue Star — Clean series names with visual hierarchy",
        [
            "Voltas product titles on collection cards read like database entries: \"VOLTAS SPLIT AIR CONDITIONER, 2 TON, 3 STAR - 243INV VECTRA ELEGANT\" — 70+ characters of all-caps technical jargon",
            "On mobile (375px), these titles wrap to 5–6 lines, pushing pricing and CTAs below the fold and making the grid feel cluttered",
            "The model code (243INV) is meaningless to consumers — it should be metadata, not the headline",
            "Blue Star uses clean, structured naming: \"G SMART WI-FI SERIES | INVERTER AC\" — series name first, type second — with tonnage and star rating as separate visual badges below",
        ],
        [
            "Restructure product titles to: \"[Series Name] [Type] — [Tonnage], [Star Rating]\" format. Example: \"Vectra Emerald Split AC — 1 Ton, 3 Star\"",
            "Move model codes to a secondary line or metadata tag — they're useful for warranty/service lookup but not for purchase decisions",
        ],
        "Growing — concise titles are becoming standard as mobile-first browsing increases",
    ),
    card(
        "Quick-add buttons on collection cards can increase add-to-cart rate by 10–15% — Voltas has no quick-add",
        "screenshots/mockup_quick_add.jpeg", "Proposed Implementation — Voltas Collection",
        "screenshots/havells_crosssell.jpeg", "Havells — \"You may also like\" cards with ATC buttons",
        [
            "Voltas collection cards have no quick-add button — users must click through to the PDP, then enter a pincode, then click Add to Cart (3+ steps vs 1 step for quick-add)",
            "The \"Add to compare\" button exists on cards but the more valuable \"Add to Cart\" / \"Quick View\" action is missing",
            "For ACs where the primary variant is tonnage (and variants aren't color/size swatches), a quick-add with variant selection popup would significantly streamline the purchase flow",
            "Havells shows \"Add to Cart\" buttons directly on product recommendation cards — enabling impulse additions with minimal friction",
        ],
        [
            "Enable Impulse theme's built-in quick-add or quick-view feature — display a \"Quick View\" popup with variant selection and ATC on collection cards",
            "Consider whether the pincode gate should apply at PDP level rather than blocking ATC entirely — show ATC on cards and validate pincode in cart/checkout instead",
        ],
        "Growing — 6/10 top electronics stores offer quick-add or quick-view on collection cards",
    ),
])

# ═══════════════════════════════════════════════════════════
# PDP (5 cards)
# ═══════════════════════════════════════════════════════════
pdp_cards = "\n".join([
    card(
        "Trust badges near the Add to Cart button increase conversion by 5–10% — Voltas PDP has no trust indicators near ATC",
        "screenshots/pdp_pincode_client.jpeg", "Voltas — PDP ATC area (no trust badges)",
        "screenshots/havells_pdp_installation.jpeg", "Havells — Free Installation badge + Loyalty Offers + Pincode check",
        [
            "The Voltas PDP ATC area shows: pincode checker, a greyed-out ATC button (until pincode validated), and \"Add to Compare\" — but zero trust badges",
            "No warranty badge, no free installation promise, no secure payment icons, no Tata guarantee — for a ₹32,000+ purchase, this is a critical trust gap",
            "The text below ATC reads \"Order once Invoiced cannot be cancelled\" and \"Refund will be credited within 14 working days\" — these are negative/restrictive messages that reduce purchase confidence instead of building it",
            "Havells shows a \"Free Installation\" badge with wrench icon, applicable offers with loyalty token earnings, and a non-blocking pincode checker — all building trust without blocking the purchase flow",
        ],
        [
            "Add 3–4 trust badges near ATC: \"Free Installation\", \"10-Year Compressor Warranty\", \"Tata Group Company\", \"Secure Payment\" — use icon + short text format",
            "Replace the negative policy text (\"cannot be cancelled\") with positive framing: \"Free Installation Included\" and \"Easy Returns within 14 Days\"",
        ],
        "Standard — 7/10 top electronics stores show trust badges near ATC (India: 5/5)",
    ),
    card(
        "Visual spec icons help buyers evaluate products 40% faster than plain text — Voltas specs are a plain bullet list",
        "screenshots/pdp_specs_client.jpeg", "Voltas — Plain text spec bullets",
        "screenshots/havells_pdp_features.jpeg", "Havells — Structured Key Features with price, dual ATC/Buy Now CTAs",
        [
            "Voltas product specs are presented as a plain unformatted bullet list: 20+ items including model number, tonnage, star rating, technical features, and manufacturer details — all in the same visual hierarchy",
            "Critical purchase-decision specs (tonnage, star rating, cooling capacity) are mixed with secondary technical details (PCB box material, hydrophilic coating) — buyers can't quickly find what matters",
            "No icon-based spec display, no tabbed organization (Specs / Description / Reviews), no comparison-friendly structured data",
            "Havells uses a \"Key Features\" heading with curated features, prominent pricing with MRP strikethrough, and dual CTA buttons (Add to Cart + Buy Now) — clear hierarchy guides the buyer's eye",
        ],
        [
            "Create a visual \"Key Specs\" section with 4–6 icon-based cards above the detailed specs: Tonnage, Star Rating, Cooling Capacity, Special Feature, Warranty, Noise Level",
            "Organize remaining specs into collapsible tabs: \"Technical Specifications\", \"Description\", \"Reviews\" — the Impulse theme supports tabbed layouts natively",
        ],
        "Standard — 9/10 top electronics stores use visual spec icons on PDPs",
    ),
    card(
        "An EMI/installment calculator on the PDP can increase conversion by 15–20% for high-AOV products — Voltas has no EMI display",
        "screenshots/mockup_emi_calc.jpeg", "Proposed Implementation — Voltas PDP",
        "screenshots/bluestar_pdp_pincode_atc.jpeg", "Blue Star — Star Rating + Tonnage selectors + Pincode + ATC + Warranty badges",
        [
            "Voltas sells ACs priced ₹32,000–75,000 — yet the PDP shows no EMI/installment option, no BNPL messaging, and no affordability nudge",
            "Simpl (Pay Later) is detected in the tech stack but is not surfaced on the PDP — the payment flexibility message is invisible to the buyer during the product evaluation stage",
            "Blue Star's PDP shows price with MRP strikethrough, Star Rating selector, Tonnage selector, Pincode checker, ATC button, and warranty badges (Lifetime Compressor + 5-Year PCB) — a comprehensive purchase decision interface",
            "A simple \"Starting at ₹X/month\" message below the price can reduce perceived cost anxiety by 30–40%",
        ],
        [
            "Add an EMI calculator widget below the price: show monthly installment for 3/6/9/12-month options with popular banks (HDFC, ICICI, SBI)",
            "Surface Simpl BNPL messaging on PDP: \"Pay in 3 interest-free installments of ₹10,667\" — place it directly below the offer price",
        ],
        "Standard — 4/5 India electronics stores show EMI/installment on PDP",
    ),
    card(
        "Low-contrast CTA buttons reduce visibility and click-through — Voltas ATC button blends into the background",
        "screenshots/pdp_pincode_client.jpeg", "Voltas — Low contrast ATC button",
        "screenshots/bluestar_pdp_top.jpeg", "Blue Star — Bold blue ATC button with clear visual hierarchy",
        [
            "The Voltas ATC button uses a thin grey/white outline style that blends into the page background — it doesn't stand out as the primary action",
            "When the pincode hasn't been entered, the ATC appears greyed out (disabled state) — this is correct behavior but the enabled state also lacks visual punch",
            "Blue Star uses a prominent blue filled ATC button that spans the full width — immediately visible and clearly the primary action on the page",
            "On mobile, the ATC needs to be the most visually prominent element on the page — Voltas's current styling makes it easy to miss",
        ],
        [
            "Restyle ATC as a filled, high-contrast button (Voltas blue #00529B or contrasting orange) with larger text — make it the most visually dominant element on mobile PDP",
            "Consider adding a \"Buy Now\" button alongside ATC for one-click direct-to-checkout — the Impulse theme supports dual CTA configuration",
        ],
        "Growing — high-contrast dual CTAs are standard on 7/10 electronics PDPs",
    ),
    card(
        "Pincode-gating the ATC button creates friction that can reduce add-to-cart rate by 20–30% — Voltas requires pincode before any cart action",
        "screenshots/pdp_pincode_client.jpeg", "Voltas — ATC disabled until pincode check",
        "screenshots/crompton_pdp_top.jpeg", "Crompton — Product info + Buy From Store CTA without pincode gate",
        [
            "Voltas completely disables the Add to Cart button until the user enters a valid pincode — the button is greyed out with no click affordance until serviceability is confirmed",
            "This creates a 3-step flow: (1) find the pincode field, (2) type 6-digit pincode, (3) click Check, (4) if serviceable, ATC becomes active — vs competitors' 1-step CTA",
            "Crompton allows immediate access to the Buy From Store action without any pincode gate — product info, color swatches, and CTAs are all immediately accessible",
            "The friction is compounded by an exchange offer checkbox that appears after pincode validation — adding yet another decision point before the user can proceed to cart",
        ],
        [
            "Make ATC always enabled — move pincode validation to the cart or checkout step where delivery address is naturally collected",
            "If serviceability check must stay on PDP, make it informational (\"Check delivery to your area\") rather than a gate that blocks the purchase flow entirely",
        ],
        "Critical — pincode-gating ATC is an anti-pattern; 9/10 competitors allow immediate ATC",
    ),
])

# ═══════════════════════════════════════════════════════════
# CART (4 cards)
# ═══════════════════════════════════════════════════════════
cart_cards = "\n".join([
    card(
        "Cross-sell recommendations in cart can increase AOV by 10–15% — Voltas cart has zero product suggestions",
        "screenshots/cart_drawer_client.jpeg", "Voltas — Cart drawer (no cross-sell)",
        "screenshots/havells_crosssell.jpeg", "Havells — \"You may also like\" cross-sell cards with ATC buttons",
        [
            "The Voltas cart drawer shows: product image, name, quantity adjuster, price, GSTIN field, Technician ID field, subtotal, policy checkbox, and checkout button — but absolutely no product recommendations",
            "For appliance purchases, cross-sell opportunities are high-value: AC stabilizer (₹2,000–4,000), installation kit, extended warranty, air purifier, etc.",
            "Havells shows a \"You may also like\" section with product cards featuring key specs and Add to Cart buttons — enabling easy accessory additions at the point of commitment",
            "The GSTIN and Technician ID fields in the cart drawer are unusual and add visual clutter for consumer buyers — these should be optional/collapsed or moved to checkout",
        ],
        [
            "Add a \"Complete Your Setup\" cross-sell section in the cart: stabilizer, extended warranty, installation accessories — these are natural complementary products with high attach rates",
            "Move GSTIN and Technician ID fields to checkout or behind an expandable \"Business Customer?\" toggle — they add friction for the 90%+ consumer buyers",
        ],
        "Standard — 8/10 top electronics stores show cross-sell in cart",
    ),
    card(
        "A free shipping threshold progress bar can increase AOV by 8–12% — Voltas cart has no shipping visibility",
        "screenshots/mockup_cart_delivery.jpeg", "Proposed Implementation — Voltas Cart",
        "screenshots/bajaj_testimonials.jpeg", "Bajaj — Customer testimonials and trust-building content throughout purchase flow",
        [
            "The Voltas cart drawer shows \"Shipping, taxes, and discount codes calculated at checkout\" — no shipping cost estimate, no free shipping threshold, no delivery timeline",
            "For ₹32,000+ appliance purchases, shipping cost uncertainty is less of an issue than delivery timeline uncertainty — when will it arrive? Is installation included?",
            "No free installation badge or delivery date is shown in the cart despite the PDP having a pincode checker with serviceability info — this context is lost in the transition to cart",
            "Competitors like Bajaj maintain confidence-building messaging throughout their purchase flow — Voltas drops all reassurance once the user reaches the cart",
        ],
        [
            "Add a delivery timeline and free installation confirmation in the cart: \"Free Installation Included · Estimated delivery: [date range]\"",
            "If a free shipping threshold exists, add a progress bar — if all orders ship free, state it explicitly: \"Free Shipping on All Orders\"",
        ],
        "Growing — delivery timeline visibility in cart reduces abandonment for high-AOV items",
    ),
    card(
        "Payment trust icons (Visa, Mastercard, UPI, RuPay) near checkout reduce payment anxiety — Voltas cart has none",
        "screenshots/cart_drawer_client.jpeg", "Voltas — Cart checkout area (no payment icons, no security badges)",
        "screenshots/mockup_payment_trust.jpeg", "Proposed Implementation — Payment trust icons below checkout button",
        [
            "The Voltas cart drawer checkout area shows only: subtotal, shipping note, policy checkbox, and a greyed-out checkout button — no payment method icons, no security badges, no trust signals",
            "For a ₹32,000+ online transaction, payment trust is critical — buyers need to see familiar payment logos (Visa, Mastercard, UPI, RuPay, Net Banking) before clicking checkout",
            "Industry best practice: payment method icons + a \"100% Secure Payment\" badge below the checkout button reduce payment anxiety and reassure buyers their transaction is safe",
            "The policy checkbox requirement adds further friction — checkout is disabled until the box is checked, and the text links to a policies page that could cause the user to leave the cart",
        ],
        [
            "Add a row of payment method icons below the checkout button: Visa, Mastercard, RuPay, UPI, Net Banking + \"100% Secure Payment\" badge with lock icon",
            "Consider making the policy acceptance implicit (with a link to policies) rather than an explicit checkbox gate — or auto-check it with a \"By proceeding, you agree to our policies\" text",
        ],
        "Standard — 7/10 top electronics stores show payment trust icons in cart",
    ),
    card(
        "The mandatory policy checkbox before checkout adds an extra step that increases cart abandonment — most stores handle this at checkout",
        "screenshots/cart_drawer_client.jpeg", "Voltas — Policy checkbox blocks checkout (greyed-out button until checked)",
        "screenshots/atomberg_cart_clean.jpeg", "Atomberg — Clean cart flow: product, coupons, delivery check, direct Checkout (no checkbox gate)",
        [
            "Voltas requires users to check \"I have read &amp; agree with the policies mentioned on this site\" before the checkout button becomes active — this is the second friction gate after the pincode requirement",
            "The checkout button is visually greyed out and disabled until the checkbox is checked — many mobile users may not understand why checkout isn't working",
            "Atomberg's cart flow is frictionless: product details → coupons &amp; offers → delivery estimation → direct Checkout button. No checkbox gate, no greyed-out button — policy acceptance is handled at the checkout/payment step",
            "Combined with the pincode-gated ATC on PDP, a Voltas buyer faces 4+ friction steps before reaching checkout: enter pincode → check serviceable → add to cart → check policy box → checkout",
        ],
        [
            "Remove the policy checkbox from the cart — move policy acceptance to checkout where Shopify handles it natively with a \"By completing this purchase, you agree to our Terms\" footer text",
            "If the checkbox must remain for legal reasons, auto-display it as checked with an option to uncheck, or use a text-based acceptance (\"By proceeding, you agree to our policies\") without a checkbox gate",
        ],
        "Anti-pattern — mandatory cart checkboxes increase abandonment; handle at checkout",
    ),
])

html = html.replace("{{FINDING_CARDS_HOMEPAGE}}", hp_cards)
html = html.replace("{{FINDING_CARDS_COLLECTION}}", col_cards)
html = html.replace("{{FINDING_CARDS_PDP}}", pdp_cards)
html = html.replace("{{FINDING_CARDS_CART}}", cart_cards)

# ── Apps HTML (14 present apps — detection March 17, 2026) ────────────
apps_present = """<div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Google Tag Manager</div>
                                    <div class="app-category">Analytics & Tracking</div>
                                    <div class="app-benchmark-tag">Container: GTM-KCPW6GW</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">GA4 (gtag.js)</div>
                                    <div class="app-category">Analytics & Tracking</div>
                                    <div class="app-benchmark-tag">Measurement ID: G-WF54WYTR46</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Facebook Pixel</div>
                                    <div class="app-category">Ads & Attribution</div>
                                    <div class="app-benchmark-tag">⚠ Duplicate Pixel ID detected — causes double-counting</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Microsoft Clarity</div>
                                    <div class="app-category">Heatmaps & Session Recording</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Klaviyo</div>
                                    <div class="app-category">Email Marketing & Automation</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Judge.me Reviews</div>
                                    <div class="app-category">Reviews & Social Proof</div>
                                    <div class="app-benchmark-tag">Installed but not added to all product page templates — inconsistent review visibility</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Razorpay</div>
                                    <div class="app-category">Payment Gateway</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Simpl Pay Later</div>
                                    <div class="app-category">BNPL / Pay Later</div>
                                    <div class="app-benchmark-tag">Installed but not surfaced on PDPs — buyers can't see BNPL option during evaluation</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Boost Commerce</div>
                                    <div class="app-category">Search & Filtering</div>
                                    <div class="app-benchmark-tag">⚠ Theme not integrated warning — filter capabilities may be limited</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">XB Wishlist</div>
                                    <div class="app-category">Wishlist & Save for Later</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">CleverTap</div>
                                    <div class="app-category">Customer Data Platform / Engagement</div>
                                    <div class="app-benchmark-tag">⚠ Invalid visitorId error in console — integration issue</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">FirstHive CDP</div>
                                    <div class="app-category">Customer Data Platform</div>
                                    <div class="app-benchmark-tag">Overlaps with CleverTap — two CDPs running simultaneously adds script overhead</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">SmartifyApps (DECO Product Labels)</div>
                                    <div class="app-category">Product Badges & Labels</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">privEzi Cookie Consent</div>
                                    <div class="app-category">Privacy & Compliance</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>"""

apps_missing = """<div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">EMI/Installment Calculator <span class="app-priority-badge critical-priority">Critical</span></div>
                                    <div class="app-category">Payment Flexibility</div>
                                    <div class="app-impact-tag conversion">📈 Conversion +15–20% for high-AOV</div>
                                    <div class="app-benchmark-tag">Standard on 4/5 India electronics stores — critical for ₹30K–75K products</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Cross-sell / Upsell App <span class="app-priority-badge critical-priority">Critical</span></div>
                                    <div class="app-category">Revenue Optimization</div>
                                    <div class="app-impact-tag revenue">💰 AOV +10–15%</div>
                                    <div class="app-benchmark-tag">Cart has zero recommendations — stabilizer, warranty, accessories are natural cross-sells</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Cart Abandonment Recovery <span class="app-priority-badge critical-priority">Critical</span></div>
                                    <div class="app-category">Revenue Recovery</div>
                                    <div class="app-impact-tag revenue">💰 Recovers 5–15% of abandoned carts</div>
                                    <div class="app-benchmark-tag">Essential for high-AOV electronics — buyers often research across sessions before committing</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Extended Warranty App <span class="app-priority-badge recommended-priority">Recommended</span></div>
                                    <div class="app-category">Post-Purchase Revenue</div>
                                    <div class="app-impact-tag revenue">💰 Post-purchase revenue +5–8%</div>
                                    <div class="app-benchmark-tag">Growing trend — Havells offers AMC/Extended Warranty as a key service</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Live Chat / WhatsApp Support <span class="app-priority-badge recommended-priority">Recommended</span></div>
                                    <div class="app-category">Customer Support</div>
                                    <div class="app-impact-tag conversion">📈 Reduces pre-purchase doubts for high-AOV</div>
                                    <div class="app-benchmark-tag">Present on 6/10 top electronics stores — critical for ₹30K+ purchase decisions</div>
                                </div>
                            </div>"""

html = html.replace("{{APPS_PRESENT_HTML}}", apps_present)
html = html.replace("{{APPS_MISSING_HTML}}", apps_missing)

# ── Strip remaining template comments ─────────────────────
html = re.sub(r'<!--\s*POPULATE:.*?-->', '', html, flags=re.DOTALL)
html = re.sub(r'<!--\s*VIDEO FINDING CARD PATTERN.*?-->', '', html, flags=re.DOTALL)
html = re.sub(r'/\*[^\n]*\{\{[A-Z_]+\}\}[^\n]*\*/', '', html)

# ── Verify no template variables remain ───────────────────
remaining = re.findall(r'\{\{[A-Z_]+\}\}', html)
if remaining:
    print(f"⚠ WARNING: {len(remaining)} unreplaced variables found:")
    for v in sorted(set(remaining)):
        print(f"   {v}")
else:
    print("✓ All template variables replaced successfully")

# ── Write output ──────────────────────────────────────────
with open(OUTPUT, "w") as f:
    f.write(html)

lines = html.count('\n') + 1
print(f"✓ Written to {OUTPUT}")
print(f"  Total lines: {lines}")
print(f"  File size: {len(html):,} bytes")
