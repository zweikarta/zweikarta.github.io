# Zweikarta & GeldSpace: SEO & Generative Engine Optimization (GEO) Master Plan

---

## 1. Why Are We Doing It? (Strategic Rationale)

### 1.1 The Studio's Core Business Objective
Zweikarta is positioned as an independent app studio in Berlin crafting calm, privacy-respecting, high-craft mobile apps. **GeldSpace** is the flagship product, addressing wealth tracking for individuals and couples.
* **Goal**: Build an organic acquisition engine that drives high-intent visitors from Google Search and AI Agents to:
  1. Learn how to handle couples finances calmly.
  2. Discover GeldSpace as the purpose-built app for the "Mine vs. Ours" philosophy.
  3. Convert readers into App Store installs and long-term active users.

### 1.2 The Dual-Engine Search Landscape (2026 Reality)
Search behavior has fragmented into two distinct engines:
1. **Traditional Organic SERP (Google)**:
   * Users search for long-tail informational and transactional queries (*e.g.*, *"how to split finances with partner without joint account"*, *"best couples net worth app"*).
   * Google evaluates sites using **E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness). Because personal finance is strictly classified as **YMYL** (*Your Money, Your Life*), anonymous or generic studio bylines struggle to rank without verified creator entities and structured data.
2. **Generative Engine Optimization (GEO) & AI Agents (Perplexity, ChatGPT Search, Gemini, Claude)**:
   * Users no longer just click links; they ask conversational, nuanced questions (*e.g.*, *"My partner and I want to track our shared wealth without sharing our separate savings. What app or method works best?"*).
   * AI engines do not rank based solely on backlink counts. They retrieve, synthesize, and **cite** sources that offer:
     * Clear, extractable entity definitions (**BLUF** — Bottom Line Up Front).
     * Authoritative structured data (`SoftwareApplication`, `FAQPage`).
     * Machine-readable summaries (`/llms.txt`).
     * Balanced, comparative analysis and original frameworks.

---

## 2. What Needs To Be Done? (Detailed Scope of Work)

The execution is split into three foundational tracks:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SCOPE OF WORK OVERVIEW                          │
├─────────────────────┬───────────────────────┬──────────────────────────┤
│ Track 1: Technical  │ Track 2: Blog Engine  │ Track 3: Content Hub     │
│ & Schema Grounding  │ Enhancements (Python) │ & Topical Clustering     │
├─────────────────────┼───────────────────────┼──────────────────────────┤
│ • SoftwareApp Schema│ • Markdown Table parser│ • 6 High-Intent Pillars  │
│ • FAQPage Schema    │ • Key Takeaways (BLUF)│ • Internal Linking Mesh  │
│ • Founder Schemas   │ • Author Entity tags  │ • Money Date Toolkit     │
│ • /llms.txt standard│ • FAQ schema generator│ • App Store CT Attribution│
└─────────────────────┴───────────────────────┴──────────────────────────┘
```

### Track 1: Technical SEO & Entity Graph Architecture
1. **`SoftwareApplication` / `MobileApplication` Schema for GeldSpace**:
   * Add comprehensive JSON-LD on `geldspace/index.html` detailing:
     * App name, category (`FinanceApplication`), pricing model (`Free`), OS (`iOS`, `Android coming soon`), screenshot links, and core capability highlights (privacy-first, no bank logins, Mine vs Ours).
2. **`FAQPage` Schema Integration**:
   * Inject schema markup for the FAQ accordion on `geldspace/index.html` (cost, bank login safety, data privacy).
3. **Founder & Organization Entity Graph (E-E-A-T)**:
   * Expand root schema in `index.html` with explicit `founder` records for Mohini (Design) and Shrikant (Mobile Development), linking skills and published apps.
4. **AI-Agent Discovery: `/llms.txt` and `/llms-full.txt`**:
   * Create standard `/llms.txt` file at the root following the open standard:
     * Concisely explains Zweikarta, its philosophy, GeldSpace's feature set, and indexed deep-dive guides for AI crawlers.

---

### Track 2: Blog Engine Upgrades (`tools/build_blog.py`)
Currently, `tools/build_blog.py` handles basic markdown, single images, and `BlogPosting` schema. To make posts rank on Google and be cited by AI agents, the builder needs:
1. **Key Takeaways / Quick Answer Block (BLUF)**:
   * Support a top-of-article summary callout designed for AI retrieval models to extract directly into answer boxes.
2. **Markdown Table Parsing**:
   * Add support for standard markdown tables (`| Col 1 | Col 2 |`). Tables are among the highest-weighted signals for AI engines comparing financial setups (*e.g.*, 50/50 split vs Proportional split vs Yours/Mine/Ours).
3. **Author Entity Mapping in Frontmatter**:
   * Allow `author: shrikant` or `author: mohini` in markdown frontmatter, linking the `BlogPosting` schema to the individual `Person` entity rather than an anonymous company byline.
4. **Article-Level FAQ Schema**:
   * Auto-detect Q&A sections or frontmatter FAQ items and generate corresponding `FAQPage` JSON-LD in the blog post's `<head>`.
5. **Cross-Article Context & Related Posts**:
   * Add an automated "Related Guides" footer to pass link equity between articles in the couples finance cluster.

---

### Track 3: Topical Authority & Content Strategy (Couples Finance)
To own the "Couples Finance" niche organically, we need a deliberate cluster of high-intent articles:

| # | Proposed Working Title | Target Intent / Search Query | GeldSpace Role |
| :--- | :--- | :--- | :--- |
| **Pillar 1** | *The 3-Account System: Yours, Mine, and Ours Explained* | "yours mine ours finance", "three account system couples" | The software implementation of the 3-account system. |
| **Pillar 2** | *How to Split Expenses Fairly (50/50 vs Proportional to Income)* | "how to split rent fairly with partner", "proportional income split calculator" | Highlighting shared net worth rather than penny-pinching. |
| **Pillar 3** | *Why Net Worth Tracking Beats Daily Expense Budgeting for Couples* | "budgeting app fatigue", "couples net worth tracker" | Direct contrast to stressful bank-linking budget apps. |
| **Pillar 4** | *Managing Money When Unmarried and Living Together* | "unmarried couples finances", "living together finances" | Safe financial clarity with total privacy intact. |
| **Pillar 5** | *The 15-Minute Monthly Money Date Checklist (Free Agenda)* | "monthly money date questions", "couples financial check in template" | GeldSpace's exact 3-question monthly ritual. |

---

## 3. How Is It Going To Impact? (Measurable Outcomes)

### 3.1 Organic Google SERP Impact
* **Rich Snippets**: The addition of `SoftwareApplication` and `FAQPage` schemas makes your Google search listings expand with interactive FAQ accordions and app details, lifting CTR by an estimated **15%–30%**.
* **YMYL Trust Unlock**: Giving author attribution to real creators with structured `Person` schemas protects the site against algorithmic quality penalties that hit anonymous finance sites.
* **Long-Tail Keyword Rankings**: Target queries that have low competition but extremely high conversion intent (*e.g.*, unmarried couples looking for wealth apps without linking bank credentials).

### 3.2 Generative Engine Optimization (GEO) & AI Agent Impact
* **Direct Recommendations in AI Search**: When users prompt Perplexity or ChatGPT (*"What is the best app for couples to track net worth without sharing private accounts?"*), the presence of `/llms.txt`, explicit feature definitions, and comparison tables allows the AI to cite GeldSpace by name with an accurate description and direct link.
* **Snippet Capture in Google AI Overviews**: Key Takeaway summary blocks directly feed the semantic extractors Google uses to populate AI Overviews at the top of search results.

### 3.3 Conversion & Studio Growth Funnel
```
Organic Searcher / AI Prompt User
               │
               ▼
   Deep-Dive Article / Guide (Trust & Value)
               │
               ▼
   In-Context Callout: "How GeldSpace makes this simple"
               │
               ▼
   App Store Listing (with ?ct=blog-<slug> campaign tag)
               │
               ▼
   High-Retention User
```

---

## 4. How Do We Test and Validate? (Verification Protocols)

We will not guess whether our optimizations are working; every change is validated against concrete standards:

### 4.1 Schema & Technical Validation
1. **Google Rich Results Test**:
   * Inspect output URLs against [Google Rich Results Test](https://search.google.com/test/rich-results) to verify `SoftwareApplication`, `FAQPage`, and `BreadcrumbList` without errors or warnings.
2. **Schema.org Validator**:
   * Validate JSON-LD graph integrity at [validator.schema.org](https://validator.schema.org/).
3. **Automated Build-Time Linting**:
   * Enhance `tools/build_blog.py` to assert that every generated page has valid canonical tags, required Open Graph dimensions, non-empty meta descriptions (120–160 chars), and valid JSON-LD structure.

### 4.2 AI Crawler & Discoverability Verification
1. **`robots.txt` & `/llms.txt` Accessibility**:
   * Verify HTTP 200 responses and clean formatting for `/llms.txt` and `/robots.txt`.
2. **AI Agent Retrieval Simulation**:
   * Query Perplexity, ChatGPT Search, and Gemini with specific long-tail prompts citing the exact terminology established in our pillar articles to benchmark citation frequency and source attribution.

### 4.3 Analytics & Attribution
1. **Google Search Console**:
   * Track impressions, average position, and clicks for queries in the "couples finance / money date / net worth" cluster.
   * Monitor indexing status of new blog URLs and rich snippet enhancements under the "Enhancements" tab.
2. **App Store Connect Campaign Tracking**:
   * Monitor referral clicks and app units via the existing `ct=blog-<slug>` and `ct=geldspace-top` campaign tokens to measure real download conversions.
