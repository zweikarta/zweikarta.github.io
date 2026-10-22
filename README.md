# zweikarta.com

Static site for the Zweikarta studio and its apps. Plain HTML and CSS, no build step. The only third-party code is Google Analytics, loaded by `assets/consent.js` only after the visitor clicks "Allow analytics". The invite and 404 pages never load it, because their URLs can carry invite codes.

## Pages
| URL | File |
|---|---|
| `/` | `index.html` (studio page) |
| `/geldspace/` | `geldspace/index.html` |
| `/geldspace/privacy/` | `geldspace/privacy/index.html` (Play Console privacy policy URL) |
| `/geldspace/delete/` | `geldspace/delete/index.html` (Play Console account deletion URL) |
| `/imprint/` | `imprint/index.html` (Impressum, § 5 DDG) |
| `/privacy/` | `privacy/index.html` (privacy notice for the website itself) |

A new app gets a folder `/<app>/` with its own `privacy/` and, if it has accounts, `delete/`.

## Analytics
Google Analytics 4 runs only with consent. The measurement ID is `GA_ID` at the top of `assets/consent.js`; while it is the placeholder `G-XXXXXXXXXX`, the script does nothing. A new page gets `<script src=".../assets/consent.js" defer></script>` in its head. If analytics changes, update `privacy/index.html` too.

## SEO
Each page has a canonical link and Open Graph tags; the home page also has Organization and WebSite structured data. When you add or change a page, add it to `sitemap.xml` (with a new `lastmod`). Pages that should stay out of search, like the invite page and the 404, carry `<meta name="robots" content="noindex">`.

## Keep in mind
1. Get the GeldSpace privacy policy reviewed by a lawyer (see `play-console/privacy-policy.md` for open assumptions A1-A8).
2. The GeldSpace privacy text comes from `play-console/privacy-policy.md`. Change both together so the website and the Play forms stay consistent.

## Hosting on GitHub Pages (free)
1. Create a **public** repo in the zweikarta organisation, e.g. `zweikarta/zweikarta.github.io`, and put these files at its root (`CNAME` and `.nojekyll` included).
2. Verify the domain first: GitHub organisation Settings › Pages › Add a domain, then add the TXT record it shows at your registrar.
3. Repo Settings › Pages: deploy from branch `main`, folder `/ (root)`. Custom domain: `zweikarta.com`.
4. At GoDaddy (Domain Portfolio › zweikarta.com › DNS), first delete the default `A @ Parked` record and the default `CNAME www` record, then add:
   - `A` for `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - `AAAA` for `@`: 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153
   - `CNAME` for `www`: `zweikarta.github.io`
5. Once the certificate is issued, tick **Enforce HTTPS**.

Source: GitHub Docs, "Managing a custom domain for your GitHub Pages site".

## Email: hello@zweikarta.com → zweikarta.dev@gmail.com (free)
Using Forward Email's free plan. Add at GoDaddy DNS:
- `MX` `@` priority 0: `mx1.forwardemail.net`
- `MX` `@` priority 0: `mx2.forwardemail.net`
- `TXT` `@`: `forward-email=hello:zweikarta.dev@gmail.com`

Note: on the free plan the TXT record is public, so the Gmail address can be looked up. Delete any other MX records GoDaddy added.

## GeldSpace screens
`assets/geldspace/*.png` are rendered from the design canvas (MktScreens artboard: OvLoanA → home-mine, OvOurs → home-ours, MonthlyHub → monthly). Re-export them when the designs change.

## Fonts
Bricolage Grotesque (SIL Open Font License, `assets/fonts/OFL.txt`) is self-hosted in `assets/fonts/`, so the site makes no requests to Google Fonts. Home and GeldSpace pages use `assets/studio.css`; legal pages use `assets/site.css`.
