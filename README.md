<!-- AUTO-GENERATED STATS UPDATE EVERY 4 HOURS - OPTIMIZED FOR GITHUB BADGES -->

<div align="center">

<img src="sntl84-banner.png" alt="SNTL84 Logo" width="220" />

<!-- TYPING_START -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=26&duration=3000&pause=1000&color=22E0B8&center=true&vCenter=true&width=650&lines=SNTL84+%C2%B7+Live+Repository+Counter;Auto-Updating+Every+4+Hours+%E2%9A%A1;75+Public+Repos+%C2%B7+Zero+Manual+Effort" alt="Typing SVG" />
<!-- TYPING_END -->

# 🔢 SNTL84 · Live Repository Counter  
### 🚀 lead-generation-service-9727413309

[![Lead Generation Service](https://img.shields.io/badge/LEAD%20GENERATION%20SERVICE-9727413309-22e0b8?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/919727413309)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-%2B91%2097274%2013309-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/919727413309)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/SNTL84/sntl84-repo-counter/update-repo-count.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/SNTL84/sntl84-repo-counter/actions)
[![Auto-Update](https://img.shields.io/badge/Auto--Update-Every%204hrs-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/SNTL84/sntl84-repo-counter/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Profile](https://img.shields.io/badge/GitHub-SNTL84-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SNTL84)
[![Website](https://img.shields.io/badge/Website-desidevloper.com-FF6B35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://desidevloper.com)
[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-22e0b8?style=for-the-badge&logo=githubpages&logoColor=white)](https://sntl84.github.io/sntl84-repo-counter/sntl84-Client-Dashboard.html)

---

### ⚡ *"I Automate What's Costing You Time."*
**Milan · SNTL 84 · AI Workflow Developer · Surat, India**

> **lead-generation-service-9727413309** — Direct WhatsApp lead line for AI automation, full-stack builds & local marketing systems.  
> 📞 **+91 97274 13309** · [Chat now](https://wa.me/919727413309)

A self-updating, zero-maintenance repository dashboard that pulls live stats straight from the GitHub REST + GraphQL APIs — no manual edits, no stale numbers, ever.

</div>

---

## 📊 Live Repository Statistics

<!-- REPO_COUNT_START -->
| Metric | Count | Details |
|--------|-------|---------|
| 🌐 Public Repos  | **75** | All public repositories |
| 🔒 Private Repos | **0** | Requires `GH_PAT` secret (repo scope) for accuracy |
| 📦 Total Repos   | **75** | Public + Private |
| ⭐ Total Stars   | **77** | Across all public repos |
| 🍴 Total Forks   | **0** | Across all public repos |
| 🏆 Top Language  | **HTML** | 24 repos |
<!-- REPO_COUNT_END -->

<!-- TIMESTAMP_START -->
> 🕐 *Last updated: **31 Oct 2026 · 14:24 UTC** · Auto-refreshes every 4 hours via GitHub Actions*
<!-- TIMESTAMP_END -->

---

## 🏗️ How It Works — At a Glance

```mermaid
flowchart LR
    A["⏰ Every 4 Hours<br/>or Push to main"] --> B[GitHub Actions Runner]
    B --> C[count_repos.py]
    C --> D[GraphQL + REST APIs]
    D --> E[Aggregate Stats]
    E --> F[Patch README.md]
    F --> G[Auto-Commit ✅]
    style A fill:#1a2a1a,stroke:#22e0b8,color:#22e0b8
    style G fill:#1a2a1a,stroke:#22e0b8,color:#22e0b8
```

---

## 🚀 Quick Start

### For Visitors
1. **Live Stats** — see the [statistics table](#-live-repository-statistics) above
2. **Interactive Dashboard** — open the [Live Dashboard](https://sntl84.github.io/sntl84-repo-counter/sntl84-Client-Dashboard.html), powered by REST + GraphQL, rendered client-side
3. **Hire SNTL84** — [message on WhatsApp](https://wa.me/919727413309) for AI automation & full-stack builds

### For Contributors
```bash
# 1. Fork & clone
git clone https://github.com/YOUR-USERNAME/sntl84-repo-counter.git

# 2. Set up environment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Run locally
export GH_TOKEN=your_token
python scripts/count_repos.py

# 4. Submit a PR 🎉
```
See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## 🔑 Unlock Accurate Private Repo Counts

> **Private repos showing `0`?** The default `GITHUB_TOKEN` can't read private repo data — add a Personal Access Token to fix it.

| Step | Action |
|------|--------|
| 1️⃣ | **GitHub → Settings → Developer Settings → Personal Access Tokens → Classic** |
| 2️⃣ | Generate a token with **`repo`** scope |
| 3️⃣ | Go to **this repo → Settings → Secrets and Variables → Actions** |
| 4️⃣ | Create a secret named **`GH_PAT`** with your token value |
| 5️⃣ | Re-run the workflow — private counts will now be accurate ✅ |

---

## 🔄 Live Dashboard API Flow

> The [dashboard](https://sntl84.github.io/sntl84-repo-counter/sntl84-Client-Dashboard.html) calls GitHub's REST & GraphQL APIs **directly from the browser** — no backend, no cache, no proxy.

```mermaid
sequenceDiagram
    participant U as 🌐 Browser
    participant R as GitHub REST API
    participant G as GitHub GraphQL API
    U->>R: GET /users/SNTL84
    U->>R: GET /users/SNTL84/repos
    U->>R: GET /users/SNTL84/events/public
    U->>G: POST /graphql (contributions)
    R-->>U: profile · repos · stars · languages
    G-->>U: contribution calendar
    U->>U: Render stat tiles, heatmap & repo cards
```

---

## ⚙️ Engine Internals

| Setting | Value |
|---------|-------|
| 🔁 Schedule | Every 4 hours |
| 🔐 Auth | `GITHUB_TOKEN` (public) + `GH_PAT` (private) |
| 🤖 Bot | SNTL84-Bot |
| 📝 Commit | `chore: auto-update repo count [skip ci]` |
| ⚡ Retry Logic | 3 attempts, exponential backoff |
| 📊 Observability | Rate-limit aware, metrics tracked |

---

## 📖 Case Study — Solving the "Stale Stats" Problem

**The problem.** A GitHub profile with 60+ repositories is hard to summarize honestly. Manually editing a README every time a repo is created, starred, or archived doesn't scale — the numbers go stale within days, and stale numbers on a developer's profile quietly undercut their credibility with recruiters, clients, and collaborators.

**The approach.** Rather than build another static badge, this project treats the README itself as a build target. A scheduled GitHub Actions workflow runs `count_repos.py` every four hours (and on every push to `main`), which queries the GitHub REST and GraphQL APIs for public repo count, star count, fork count, and top language, then patches the numbers directly between HTML comment markers in `README.md` and commits the change back automatically.

**The tech stack.** Python 3.11+ for the counting script, GitHub Actions for scheduling and compute, the GitHub REST + GraphQL APIs for data, and a lightweight client-side dashboard (`sntl84-Client-Dashboard.html`) that calls the same APIs directly from the browser for a live, interactive view — no backend server, no database, no cache layer to maintain.

**The result.** Zero manual maintenance. The stats table, the timestamp, and the repository list all update themselves on a fixed cadence with retry logic and exponential backoff for reliability. For visitors, that means every number on this page is current as of the last four hours — not the last time someone remembered to edit a README.

**Why it matters beyond this repo.** The same pattern — treat documentation as a build artifact, not a hand-edited file — is the basis for the automation work SNTL84 builds for clients: WhatsApp-driven registration flows, auto-refreshing dashboards, and reporting pipelines that remove a human from the update loop entirely.

---

## ❓ FAQ — Purpose of This Repository

**Q: What does this repository actually do?**
A: It keeps a live, auto-updating count of SNTL84's public GitHub repositories — total repos, stars, forks, and top language — displayed right in this README, with no manual editing required.

**Q: How often do the stats refresh?**
A: Every 4 hours automatically via a scheduled GitHub Actions workflow, and immediately on any push to `main`.

**Q: Where do the numbers come from?**
A: Directly from the GitHub REST and GraphQL APIs — the same data GitHub itself uses, queried live by `count_repos.py`.

**Q: Is there a visual dashboard, or just this table?**
A: Both. The table above lives in this README, and a full interactive [Live Dashboard](https://sntl84.github.io/sntl84-repo-counter/sntl84-Client-Dashboard.html) renders stat tiles, a contribution heatmap, and repo cards client-side in the browser.

**Q: Why is the private repo count showing 0?**
A: The default `GITHUB_TOKEN` GitHub Actions provides can't read private repo data. Adding a personal access token as a `GH_PAT` secret (see the [Unlock Accurate Private Repo Counts](#-unlock-accurate-private-repo-counts) section) fixes this.

**Q: Can I reuse this for my own GitHub profile?**
A: Yes — fork the repo, follow the [Quick Start](#-quick-start) steps for contributors, point it at your own username, and the same workflow will maintain your own live stats table.

**Q: What's the tech stack?**
A: Python 3.11+ for the counting logic, GitHub Actions for scheduling, and the GitHub REST + GraphQL APIs for data — no external database or hosting required.

**Q: Who built this, and why?**
A: Milan (SNTL84), an AI workflow developer based in Surat, India, who builds automation that removes repetitive manual work — this repo is a small, public example of that same philosophy applied to his own GitHub profile.

**Q: How do I get in touch about custom automation work?**
A: [Message SNTL84 on WhatsApp](https://wa.me/919727413309) or visit [desidevloper.com](https://desidevloper.com).

---

## 📁 All Public Repositories

<!-- REPO_LIST_START -->
| # | Repository | Description | Language | ⭐ | 🍴 | Updated |
|---|------------|-------------|----------|----|----|---------|
| 1 | [sntl84-repo-counter-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-repo-counter-lead-generation-service-9727413309) | 🔢 Auto-updating repo counter for SNTL84 · Milan · desidevloper.com — live count of al | 🌐 HTML | ⭐1 | — | 2026-10-31 |
| 2 | [metromate-website-roadmap-lead-generation-service-9727413309](https://github.com/SNTL84/metromate-website-roadmap-lead-generation-service-9727413309) | 🚀 Complete Website Development Roadmap for Tragad Soni ｜ AI-Powered Automation ｜ Supp | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 3 | [sntl84-next-saas-stripe-starter-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-next-saas-stripe-starter-lead-generation-service-9727413309) | SaaS Starter with User Roles & Admin Panel — Private fork by SNTL 84 · Milan · Automa | 🔷 TS | ⭐1 | — | 2026-10-30 |
| 4 | [sntl84](https://github.com/SNTL84/sntl84) | — | — | ⭐1 | — | 2026-10-30 |
| 5 | [whatsapp-business-chat-agent-lead-generation-service-9727413309](https://github.com/SNTL84/whatsapp-business-chat-agent-lead-generation-service-9727413309) | 🚀 Flagship: Configure your WhatsApp Business Chat Agent in Express mode for just ₹999 | — | ⭐1 | — | 2026-10-30 |
| 6 | [whatsapp-outreach-tool-lead-generation-service-9727413309](https://github.com/SNTL84/whatsapp-outreach-tool-lead-generation-service-9727413309) | ⚡ Zero-install WhatsApp Outreach Tool — Bulk contact management, custom messages, VCF | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 7 | [ts-type-mastery-lead-generation-service-9727413309](https://github.com/SNTL84/ts-type-mastery-lead-generation-service-9727413309) | 🔥 TypeScript Type Challenges — Elite solutions, annotated mental models & reusable ty | 🔷 TS | ⭐1 | — | 2026-10-30 |
| 8 | [trade-directory-lead-generation-service-9727413309](https://github.com/SNTL84/trade-directory-lead-generation-service-9727413309) | — | 🌐 HTML | — | — | 2026-10-30 |
| 9 | [sntl84bulkautomation-blaster-tools-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84bulkautomation-blaster-tools-lead-generation-service-9727413309) | WhatsApp & Aratt.ai Bulk Outreach Automation Tools by SNTL84 ｜ AI Workflow Profession | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 10 | [sntl84-shopify-leadgen-proposal-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-shopify-leadgen-proposal-lead-generation-service-9727413309) | Automate What's Costing You Money — Shopify AI Automation & Growth Systems for D2C Br | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 11 | [sntl84-shiv-gujarati-thali-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-shiv-gujarati-thali-lead-generation-service-9727413309) | 🍽️ Full-stack digital presence for Shiv Gujarati Unlimited Thali, Surat — Landing pag | 🐚 Shell | ⭐1 | — | 2026-10-30 |
| 12 | [sntl84-service-catalog-v1-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-service-catalog-v1-lead-generation-service-9727413309) | 🗂️ Service Catalog V1 — 48 AI & Digital Services by SNTL84 ｜ AI Workflow · Web Dev ·  | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 13 | [sntl84-resume-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-resume-lead-generation-service-9727413309) | I Automate What's Costing You Money. · Milan · SNTL 84 · AI Workflow Professional · S | — | ⭐1 | — | 2026-10-30 |
| 14 | [sntl84-real-estate-claude-agent-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-real-estate-claude-agent-lead-generation-service-9727413309) | AI-powered property valuation & investment analysis for Surat, Gujarat — SNTL84 Frame | 🔷 TS | ⭐1 | — | 2026-10-30 |
| 15 | [sntl84-python-foundations-projects-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-python-foundations-projects-lead-generation-service-9727413309) | 🐍 Python Foundations — CLI Projects by Milan · SNTL 84 ｜ I Automate What's Costing Yo | 🐍 Python | ⭐1 | — | 2026-10-30 |
| 16 | [sntl84-multilingual-statement-generator-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-multilingual-statement-generator-lead-generation-service-9727413309) | Client Conversion Statements Multilingual Generator — 29 statements · 39 languages ·  | 🌐 HTML | ⭐2 | — | 2026-10-30 |
| 17 | [sntl84-megait-stores-client-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-megait-stores-client-lead-generation-service-9727413309) | 🖥️ MEGA IT STORES — Full Client Digital Package ｜ Product Catalog + Performance Marke | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 18 | [sntl84-linkedin-activity-archive-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-linkedin-activity-archive-lead-generation-service-9727413309) | Complete LinkedIn activity archive for SNTL2784 - Posts, reposts, media links, analyt | — | ⭐1 | — | 2026-10-30 |
| 19 | [sntl84-hiring-system-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-hiring-system-lead-generation-service-9727413309) | AI-Powered Hiring System — Smart Job Board & Candidate Portal by SNTL 84 ｜ Vercel-Rea | — | ⭐1 | — | 2026-10-30 |
| 20 | [sntl84-growth-engine-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-growth-engine-lead-generation-service-9727413309) | 🚀 SNTL 84 — Your Growth Engine ｜ Lead Gen • AI Automation • Fulfillment • Bench Resou | — | ⭐3 | — | 2026-10-30 |
| 21 | [sntl84-fmcg-lead-intel-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-fmcg-lead-intel-lead-generation-service-9727413309) | 🧠 FMCG Lead Intelligence Engine — n8n + Claude AI. Automates distributor outreach: sc | — | ⭐1 | — | 2026-10-30 |
| 22 | [sntl84-enterprise-ai-services-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-enterprise-ai-services-lead-generation-service-9727413309) | 🚀 Enterprise AI Automation & Workflow Solutions — Premium services in AI workflow dev | — | ⭐1 | — | 2026-10-30 |
| 23 | [sntl84-ecom-store-setup-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-store-setup-lead-generation-service-9727413309) | 🛒 Service 01 — Full eCommerce Store Setup ｜ Shopify · WooCommerce · Custom Stack ｜ SN | — | ⭐1 | — | 2026-10-30 |
| 24 | [sntl84-ecom-seo-optimization-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-seo-optimization-lead-generation-service-9727413309) | 🔎 Service 07 — eCommerce SEO Optimization ｜ Google Rank · On-Page · Technical SEO ｜ S | — | ⭐1 | — | 2026-10-30 |
| 25 | [sntl84-ecom-product-sourcing-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-product-sourcing-lead-generation-service-9727413309) | 🔍 Service 04 — Product Sourcing ｜ Supplier Vetting · Margin Protection · India & Asia | — | ⭐1 | — | 2026-10-30 |
| 26 | [sntl84-ecom-returns-mgmt-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-returns-mgmt-lead-generation-service-9727413309) | ↩️ Service 10 — Returns & RTO Management ｜ Automated Returns · Refunds · RTO Recovery | — | ⭐1 | — | 2026-10-30 |
| 27 | [sntl84-ecom-payment-integration-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-payment-integration-lead-generation-service-9727413309) | 💳 Service 06 — Payment Integration ｜ Razorpay · Paytm · UPI · Stripe · COD ｜ SNTL84 D | — | ⭐1 | — | 2026-10-30 |
| 28 | [sntl84-ecom-order-fulfillment-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-order-fulfillment-lead-generation-service-9727413309) | 🚚 Service 05 — Order Fulfillment Automation ｜ Shiprocket · Delhivery · End-to-End Ops | — | ⭐1 | — | 2026-10-30 |
| 29 | [sntl84-ecom-marketplace-listing-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-marketplace-listing-lead-generation-service-9727413309) | 🏪 Service 03 — Marketplace Listing Management ｜ Amazon · Flipkart · Meesho · A+ Conte | — | ⭐1 | — | 2026-10-30 |
| 30 | [sntl84-ecom-inventory-sync-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-inventory-sync-lead-generation-service-9727413309) | 🔄 Service 09 — Inventory Sync & Management ｜ Real-Time Stock · Multi-Channel · EasyEc | — | ⭐1 | — | 2026-10-30 |
| 31 | [sntl84-ecom-dropshipping-setup-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-dropshipping-setup-lead-generation-service-9727413309) | 📦 Service 02 — Dropshipping Setup ｜ Supplier Sourcing · Store Automation · ₹0 Invento | — | ⭐1 | — | 2026-10-30 |
| 32 | [sntl84-ecom-customer-support-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-customer-support-lead-generation-service-9727413309) | 🎧 Service 11 — Customer Support Setup ｜ WhatsApp · Chatbot · Helpdesk · CRM ｜ SNTL84  | — | ⭐1 | — | 2026-10-30 |
| 33 | [sntl84-dev-profile-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-dev-profile-lead-generation-service-9727413309) | Automate What's Costing You Money. SNTL 84 Developer Profile + Python Journey Tracker | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 34 | [sntl84-ecom-ad-campaigns-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ecom-ad-campaigns-lead-generation-service-9727413309) | 📣 Service 08 — Ad Campaign Management ｜ Google · Meta · Instagram · Performance Marke | — | ⭐1 | — | 2026-10-30 |
| 35 | [sntl84-desidevloper-live-demo-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-desidevloper-live-demo-lead-generation-service-9727413309) | 🚀 Live Demo — Services by desidevloper.com ｜ AI Systems · Full-Stack Builds · Supply  | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 36 | [sntl84-desidevloper-services-page-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-desidevloper-services-page-lead-generation-service-9727413309) | Desi devloper Services page  | — | ⭐1 | — | 2026-10-30 |
| 37 | [sntl84-desidevloper-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-desidevloper-lead-generation-service-9727413309) | We learn everyday to think with our tools. ｜ AI Workflow Developer · Automation-Drive | — | ⭐1 | — | 2026-10-30 |
| 38 | [sntl84-desi-quote-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-desi-quote-lead-generation-service-9727413309) | ⚡ DesiQuote — Instant Gig Quote Calculator by Milan · SNTL 84 · desidevloper.com ｜ AI | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 39 | [sntl84-cohost-virtual-assistant-v3-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-cohost-virtual-assistant-v3-lead-generation-service-9727413309) | SNTL 84 Co-Host Virtual Assistant V3 — Premium AI-powered property management landing | 🌐 HTML | ⭐2 | — | 2026-10-30 |
| 40 | [sntl84-business-intelligence-push-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-business-intelligence-push-lead-generation-service-9727413309) | 🧠 Service Master with Deep BI — 264 Services · 22 Industry Categories · Full B2B Trad | — | ⭐1 | — | 2026-10-30 |
| 41 | [sntl84-backoffice-os-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-backoffice-os-lead-generation-service-9727413309) | 🏢 BACKOFFICE OS v2.0 — A small utility HR back-office dashboard. Attendance, payroll, | 🌐 HTML | ⭐2 | — | 2026-10-30 |
| 42 | [sntl84-agentic-recruiter-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-agentic-recruiter-lead-generation-service-9727413309) | 🤖 AI-Powered Recruitment Screening Module ｜ Automate What's Costing You Money ｜ Reduc | 🌐 HTML | ⭐2 | — | 2026-10-30 |
| 43 | [sntl84-ai-hiring-intel-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-ai-hiring-intel-lead-generation-service-9727413309) | AI Hiring Intelligence System — Strict, business-focused resume evaluator. Built by M | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 44 | [open-issue-triage-lead-generation-service-9727413309](https://github.com/SNTL84/open-issue-triage-lead-generation-service-9727413309) | 🔧 Open Source Issue Triage — Maintainer-style responses to GitHub issues across the e | — | ⭐1 | — | 2026-10-30 |
| 45 | [radhey-jewels-metromate-business-setup-lead-generation-service-9727413309](https://github.com/SNTL84/radhey-jewels-metromate-business-setup-lead-generation-service-9727413309) | 🌟 Case Study: Radhey Jewels (Imitation Jewellery) — Complete WhatsApp, Instagram & Fa | — | ⭐1 | — | 2026-10-30 |
| 46 | [ramdevcab-lead-generation-service-9727413309](https://github.com/SNTL84/ramdevcab-lead-generation-service-9727413309) | 🚖 Ramdev Cab Taxi Service, Surat: digital launch kit by SNTL 84 ｜ Automate What's Cos | 🐚 Shell | ⭐1 | — | 2026-10-30 |
| 47 | [n8n-india-smb-workflow-templates-lead-generation-service-9727413309](https://github.com/SNTL84/n8n-india-smb-workflow-templates-lead-generation-service-9727413309) | 🤖 Ready-to-import n8n workflow templates for Indian SMBs — WhatsApp leads, GST invoic | — | ⭐1 | — | 2026-10-30 |
| 48 | [metromate-shiv-kathiawadi-thali-brand-development-lead-generation-service-9727413309](https://github.com/SNTL84/metromate-shiv-kathiawadi-thali-brand-development-lead-generation-service-9727413309) | 🍛 Complete Brand Development Case Study — MetroMate Real Marketing × Shiv Kathiawadi  | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 49 | [metromate-performance-marketing-lead-generation-service-9727413309](https://github.com/SNTL84/metromate-performance-marketing-lead-generation-service-9727413309) | MetroMate Performance Marketing — social media account cleanup, fulfillment automatio | — | ⭐1 | — | 2026-10-30 |
| 50 | [mads-metro-ad-services-lead-generation-service-9727413309](https://github.com/SNTL84/mads-metro-ad-services-lead-generation-service-9727413309) | MADS (Metro Ad Services) — cycle advertising business plan, operations dashboard, and | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 51 | [metromate-mahadev-restaurant-pal-surat-case-study-lead-generation-service-9727413309](https://github.com/SNTL84/metromate-mahadev-restaurant-pal-surat-case-study-lead-generation-service-9727413309) | MetroMate Performance Marketing — Full-scale launch of Mahadev Restaurant's new branc | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 52 | [earth-elements-business-setup-lead-generation-service-9727413309](https://github.com/SNTL84/earth-elements-business-setup-lead-generation-service-9727413309) | Case Study: Earth Elements (Numerology • Crystal • Gemstone) — Google Business Profil | — | ⭐1 | — | 2026-10-30 |
| 53 | [metromate-lead-generation-service-9727413309](https://github.com/SNTL84/metromate-lead-generation-service-9727413309) | 🏢 ResidentialParkingManagementServices ｜ Automate What's Costing You Money ｜ SNTL 84  | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 54 | [desidevloper-lead-generation-service-9727413309](https://github.com/SNTL84/desidevloper-lead-generation-service-9727413309) | DesiDeveloper - Full-stack React portfolio & trade directory platform with Vite, Reac | — | ⭐1 | — | 2026-10-30 |
| 55 | [coral-heights-vehicle-registration-lead-generation-service-9727413309](https://github.com/SNTL84/coral-heights-vehicle-registration-lead-generation-service-9727413309) | Smart WhatsApp-based vehicle registration form for Coral Heights Society A-Wing. Buil | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 56 | [bust-the-ghost-labour-lead-generation-service-9727413309](https://github.com/SNTL84/bust-the-ghost-labour-lead-generation-service-9727413309) | A community list exposing anonymous 'ghost labour' practices where developers connect | — | ⭐1 | — | 2026-10-30 |
| 57 | [desidevloper-portfolio-nextjs-lead-generation-service-9727413309](https://github.com/SNTL84/desidevloper-portfolio-nextjs-lead-generation-service-9727413309) | 🚀 desidevloper.com — Next.js 14 + TypeScript + TailwindCSS + Framer Motion portfolio. | 🔷 TS | ⭐1 | — | 2026-10-30 |
| 58 | [ai-studio-99page-generator-lead-generation-service-9727413309](https://github.com/SNTL84/ai-studio-99page-generator-lead-generation-service-9727413309) | 99 Page in 3 prompts | 🔷 TS | ⭐1 | — | 2026-10-30 |
| 59 | [ai-lead-enrichment-agent-lead-generation-service-9727413309](https://github.com/SNTL84/ai-lead-enrichment-agent-lead-generation-service-9727413309) | 🚀 AI Lead Enrichment Agent – Enrich startup leads with founder names, funding stages, | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 60 | [automate-what-costs-you-lead-generation-service-9727413309](https://github.com/SNTL84/automate-what-costs-you-lead-generation-service-9727413309) | 🚀 AI Automation Toolkit by Milan · SNTL 84 — Workflows, Bots & Business Intelligence  | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 61 | [ai-frontend-projects-lead-generation-service-9727413309](https://github.com/SNTL84/ai-frontend-projects-lead-generation-service-9727413309) | 45 battle-tested AI frontend builds · real revenue targets · ship-ready code · OpenAI | 🌐 HTML | ⭐1 | — | 2026-10-30 |
| 62 | [youtube-agent-skill-lead-generation-service-9727413309](https://github.com/SNTL84/youtube-agent-skill-lead-generation-service-9727413309) | Eleven Claude skills that run a YouTube channel: scripts off 21 hook formulas with a  | — | — | — | 2026-10-30 |
| 63 | [wacrm-lead-generation-service-9727413309](https://github.com/SNTL84/wacrm-lead-generation-service-9727413309) | Self-hostable CRM template for WhatsApp — shared inbox, contacts, sales pipelines, br | — | — | — | 2026-10-30 |
| 64 | [velocity-lead-generation-service-9727413309](https://github.com/SNTL84/velocity-lead-generation-service-9727413309) | 🚀🪐🌕🌑☄️🛸 Opensource equivalent of Google's Antigravity/Claude Code/Cursor | — | ⭐1 | — | 2026-10-30 |
| 65 | [undici-lead-generation-service-9727413309](https://github.com/SNTL84/undici-lead-generation-service-9727413309) | An HTTP/1.1 client, written from scratch for Node.js | — | ⭐1 | — | 2026-10-30 |
| 66 | [sntl84-superpowers-lead-generation-service-9727413309](https://github.com/SNTL84/sntl84-superpowers-lead-generation-service-9727413309) | An agentic skills framework & software development methodology that works. | 🐚 Shell | ⭐1 | — | 2026-10-30 |
| 67 | [ruflo-lead-generation-service-9727413309](https://github.com/SNTL84/ruflo-lead-generation-service-9727413309) | 🌊 The leading agent meta-harness for Claude. Deploy intelligent multi-agent swarms, c | — | ⭐1 | — | 2026-10-30 |
| 68 | [reelmimic-lead-generation-service-9727413309](https://github.com/SNTL84/reelmimic-lead-generation-service-9727413309) | Show it a video you love. Get a new video in the same style. An AI crew (Claude Code  | — | ⭐1 | — | 2026-10-30 |
| 69 | [react-lead-generation-service-9727413309](https://github.com/SNTL84/react-lead-generation-service-9727413309) | The library for web and native user interfaces. | — | ⭐1 | — | 2026-10-30 |
| 70 | [net-merge-lead-generation-service-9727413309](https://github.com/SNTL84/net-merge-lead-generation-service-9727413309) | Use all your network adapters at once on Windows/Linux/Mac: per-connection load balan | — | ⭐1 | — | 2026-10-30 |
| 71 | [indian-food-image-dataset-lead-generation-service-9727413309](https://github.com/SNTL84/indian-food-image-dataset-lead-generation-service-9727413309) | 🍛 Open dataset of Indian food images for AI/ML — built for classification, detection  | — | ⭐1 | — | 2026-10-30 |
| 72 | [cal-diy-lead-generation-service-9727413309](https://github.com/SNTL84/cal-diy-lead-generation-service-9727413309) | Scheduling infrastructure for absolutely everyone. | — | ⭐1 | — | 2026-10-30 |
| 73 | [awesome-ai-sales-agents-lead-generation-service-9727413309](https://github.com/SNTL84/awesome-ai-sales-agents-lead-generation-service-9727413309) | A curated Awesome list of AI SDR and autonomous sales agent tools — for founders, sal | — | ⭐1 | — | 2026-10-30 |
| 74 | [api-cookbook-lead-generation-service-9727413309](https://github.com/SNTL84/api-cookbook-lead-generation-service-9727413309) | A collection of projects and guides with Perplexity's API Platform | — | — | — | 2026-10-30 |
| 75 | [shopify-leadgen-proposal](https://github.com/SNTL84/shopify-leadgen-proposal) | Premium Shopify Development & AI Automation — Lead Generation Proposal by desidevlope | — | ⭐1 | — | 2026-04-29 |
| — | *Private repos* | *0 detected — add GH_PAT secret (repo scope) if you have private repos* | 🔒 Private | — | — | — |
<!-- REPO_LIST_END -->