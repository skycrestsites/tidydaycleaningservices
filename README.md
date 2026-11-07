# Tidy Day Cleaning Services website

Static, mobile-first site for Tidy Day Cleaning Services (owner: Kirsten Thouvenot), serving Austin, TX and surrounding areas.

## Pages (clean URLs, no .html)
- `/` home
- `/services/` all services
- `/services/<service>/` one page per service (7 total)
- `/about/`
- `/contact/` quote form (`/contact/?service=<slug>` preselects a service)

Every page is an `index.html` inside its own folder, and internal links are relative, so any static host (GitHub Pages, Netlify, Vercel, Cloudflare Pages) serves `/services/deep-cleaning/` without `.html`.

## Editing
All copy lives in `_src/content.py` (services, FAQs, areas, contact details). Templates are in `_src/build.py`. After editing run:

    python _src/build.py

Styles: `css/styles.css`. Behavior: `js/main.js`. Images: `assets/img/`.

## Before going live
1. Domain: canonicals, Open Graph, JSON-LD, `sitemap.xml` and `robots.txt` use `https://www.tidydaycleaning.com`. Change `SITE` in `_src/content.py` if different and rebuild.
2. Contact: confirm `EMAIL` and add `PHONE` in `_src/content.py` (phone links stay hidden while blank).
3. Quote form currently opens the visitor's email app pre-filled. To collect submissions directly, hook it to Formspree or similar.
4. Swap stock photos for real job photos when available (keep file names).
5. Add the site to Google Search Console and Google Business Profile.
