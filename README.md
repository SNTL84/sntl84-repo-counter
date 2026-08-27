<!-- AUTO-GENERATED STATS UPDATE EVERY 4 HOURS - OPTIMIZED FOR GITHUB BADGES -->

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=26&duration=3000&pause=1000&color=22E0B8&center=true&vCenter=true&width=650&lines=SNTL84+%C2%B7+Live+Repository+Counter;Auto-Updating+Every+4+Hours+%E2%9A%A1;61%2B+Repos+%C2%B7+Zero+Manual+Effort" alt="Typing SVG" />

# 🔢 SNTL84 · Live Repository Counter

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

A self-updating, zero-maintenance repository dashboard that pulls live stats straight from the GitHub REST + GraphQL APIs — no manual edits, no stale numbers, ever.

</div>

---

## 📊 Live Repository Statistics

<!-- REPO_COUNT_START -->
| Metric | Count | Details |
|--------|-------|---------|
| 🌐 Public Repos  | **64** | All public repositories |
| 🔒 Private Repos | **0** | Requires `GH_PAT` secret (repo scope) for accuracy |
| 📦 Total Repos   | **64** | Public + Private |
| ⭐ Total Stars   | **61** | Across all public repos |
| 🍴 Total Forks   | **0** | Across all public repos |
| 🏆 Top Language  | **HTML** | 22 repos |
<!-- REPO_COUNT_END -->

<!-- TIMESTAMP_START -->
> 🕐 *Last updated: **27 Aug 2026 · 08:28 UTC** · Auto-refreshes every 4 hours via GitHub Actions*
<!-- TIMESTAMP_END -->

---

## 🏗️ How It Works — At a Glance

```mermaid
flowchart LR
    A[⏰ Every 4 Hours\nor Push to main] --> B[GitHub Actions Runner]
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

## 📁 All Public Repositories

<!-- REPO_LIST_START -->
