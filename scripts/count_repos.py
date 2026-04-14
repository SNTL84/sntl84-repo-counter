#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

Accuracy notes:
  PUBLIC  → paginated /users/SNTL84/repos (all public repos)
  PRIVATE → /user endpoint → owned_private_repos field
            Requires GH_PAT (classic token, repo scope) for accurate private count.
            GITHUB_TOKEN (default Actions token) only sees repos in current repo context,
            so owned_private_repos may return 0 unless GH_PAT is set.
  TOTAL   → public + private

Local usage:
  GH_TOKEN=ghp_yourToken python3 scripts/count_repos.py
"""
import os
import re
import requests
from datetime import datetime, timezone

TOKEN = os.environ.get("GH_TOKEN", "") or os.environ.get("GITHUB_TOKEN", "")
USER  = "SNTL84"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def gh_get(url, params=None, auth=True):
    headers = HEADERS if auth else {"Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    if r.status_code != 200:
        print(f"[ERROR] GET {url} → {r.status_code}: {r.text[:300]}")
        r.raise_for_status()
    return r.json()


def fetch_public_repos():
    """Paginate ALL public repos for USER."""
    repos, page = [], 1
    while True:
        batch = gh_get(
            f"https://api.github.com/users/{USER}/repos",
            params={"per_page": 100, "page": page, "sort": "updated"},
            auth=False,
        )
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    print(f"[REST] Fetched {len(repos)} public repos via /users/{USER}/repos")
    return repos


def get_private_count():
    """
    Fetch private repo count via /user endpoint.
    IMPORTANT: This REQUIRES GH_PAT (classic token with 'repo' scope) set as a
    repository secret. The default GITHUB_TOKEN does NOT have permission to read
    owned_private_repos for the account — it will return 0.

    Steps to fix private count:
      1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Classic
      2. Generate token with 'repo' scope
      3. Go to this repo → Settings → Secrets → Actions → New secret
      4. Name: GH_PAT, Value: your token
    """
    if not TOKEN:
        print("[WARN] No token set — private count will be 0.")
        return 0, "unknown"
    try:
        data = gh_get("https://api.github.com/user", auth=True)
        login         = data.get("login", "unknown")
        private_count = data.get("owned_private_repos", 0)
        total_private = data.get("total_private_repos", 0)
        print(f"[REST /user] login={login}")
        print(f"[REST /user] owned_private_repos={private_count}  total_private_repos={total_private}")
        # If owned_private_repos=0 but total_private_repos>0, token may lack scope
        if private_count == 0 and total_private > 0:
            print("[WARN] owned_private_repos=0 but total_private_repos>0.")
            print("[WARN] Your GH_PAT may lack 'repo' scope. Using total_private_repos as fallback.")
            return total_private, login
        return private_count, login
    except Exception as e:
        print(f"[ERROR] /user fetch failed: {e}")
        return 0, "unknown"


def language_badge(lang):
    """Return a short emoji+text badge for common languages."""
    badges = {
        "Python": "🐍 Python", "JavaScript": "🟨 JS", "TypeScript": "🔷 TS",
        "HTML": "🌐 HTML", "CSS": "🎨 CSS", "Shell": "🐚 Shell",
        "Java": "☕ Java", "Go": "🐹 Go", "Rust": "🦀 Rust",
        "Ruby": "💎 Ruby", "PHP": "🐘 PHP", "C++": "⚙️ C++",
    }
    return badges.get(lang, f"📄 {lang}" if lang else "—")


def main():
    # 1. Fetch counts
    public_repos          = fetch_public_repos()
    public_count          = len(public_repos)
    private_count, login  = get_private_count()
    total_count           = public_count + private_count
    date_str              = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    date_display          = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")

    print(f"\n📊 Final Count:")
    print(f"  🌐 Public:  {public_count}")
    print(f"  🔒 Private: {private_count}")
    print(f"  📦 Total:   {total_count}\n")

    # 2. Build repo list rows
    rows = []
    for i, r in enumerate(public_repos, 1):
        name  = r["name"]
        url   = r["html_url"]
        desc  = (r.get("description") or "—")[:85].replace("|", "｜")
        lang  = language_badge(r.get("language"))
        stars = r.get("stargazers_count", 0)
        forks = r.get("forks_count", 0)
        date  = (r.get("updated_at") or "")[:10]
        star_str = f"⭐{stars}" if stars > 0 else "—"
        fork_str = f"🍴{forks}" if forks > 0 else "—"
        rows.append(
            f"| {i} | [{name}]({url}) | {desc} | {lang} | {star_str} | {fork_str} | {date} |"
        )

    if private_count > 0:
        label = f"{private_count} private repo{'s' if private_count != 1 else ''}"
        rows.append(
            f"| — | *{label}* | *Kept private — not listed* | 🔒 Private | — | — | — |"
        )
    else:
        rows.append("| — | *Private repos* | *0 private repos (or GH_PAT not set)* | 🔒 Private | — | — | — |")

    repo_table = "\n".join(rows)

    # 3. Calculate stats
    languages = {}
    for r in public_repos:
        lang = r.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    total_stars = sum(r.get("stargazers_count", 0) for r in public_repos)
    total_forks = sum(r.get("forks_count", 0) for r in public_repos)
    top_lang = max(languages, key=languages.get) if languages else "—"
    top_lang_count = languages.get(top_lang, 0)

    # 4. Build README blocks
    count_block = (
        "<!-- REPO_COUNT_START -->\n"
        "| Metric | Count | Details |\n"
        "|--------|-------|---------|\n"
        f"| 🌐 Public Repos  | **{public_count}** | All public repositories |\n"
        f"| 🔒 Private Repos | **{private_count}** | Requires `GH_PAT` secret (repo scope) for accuracy |\n"
        f"| 📦 Total Repos   | **{total_count}** | Public + Private |\n"
        f"| ⭐ Total Stars   | **{total_stars}** | Across all public repos |\n"
        f"| 🍴 Total Forks   | **{total_forks}** | Across all public repos |\n"
        f"| 🏆 Top Language  | **{top_lang}** | {top_lang_count} repos |\n"
        "<!-- REPO_COUNT_END -->"
    )

    list_block = (
        "<!-- REPO_LIST_START -->\n"
        "| # | Repository | Description | Language | ⭐ | 🍴 | Updated |\n"
        "|---|------------|-------------|----------|----|----|---------|\n"
        f"{repo_table}\n"
        "<!-- REPO_LIST_END -->"
    )

    timestamp_block = (
        f"<!-- TIMESTAMP_START -->\n"
        f"> 🕐 *Last updated: **{date_display}** · Auto-refreshes every 6 hours via GitHub Actions*\n"
        f"<!-- TIMESTAMP_END -->"
    )

    # 5. Patch README — each block independently
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    new_readme, n1 = re.subn(
        r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->",
        count_block, readme, flags=re.DOTALL,
    )
    if n1 == 0:
        print("[WARN] REPO_COUNT markers not found — appending.")
        new_readme = readme + "\n" + count_block + "\n"

    new_readme, n2 = re.subn(
        r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
        list_block, new_readme, flags=re.DOTALL,
    )
    if n2 == 0:
        print("[WARN] REPO_LIST markers not found.")

    new_readme, n3 = re.subn(
        r"<!-- TIMESTAMP_START -->.*?<!-- TIMESTAMP_END -->",
        timestamp_block, new_readme, flags=re.DOTALL,
    )
    if n3 == 0:
        print("[WARN] TIMESTAMP markers not found.")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"✅ README.md updated — {total_count} total repos · {date_str}")
    print(f"   Blocks patched: count={n1}, list={n2}, timestamp={n3}")


if __name__ == "__main__":
    main()
