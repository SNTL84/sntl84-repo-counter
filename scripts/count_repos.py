#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

Runs as GitHub Action every 6 hrs to:
  1. Count all repos (public + private) via GitHub API
  2. List ALL repos with name, description, type, language, date
  3. Update README.md between marker comments
  4. Bot commits the change

Local usage:
  GH_TOKEN=your_pat python3 scripts/count_repos.py
"""

import os
import re
import requests
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────
TOKEN = os.environ.get("GH_TOKEN", "")
USER  = "SNTL84"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# ── Helpers ───────────────────────────────────────────────────
def gh_get(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def fetch_all_repos():
    """Paginate through all repos (public + private) for authenticated user."""
    repos, page = [], 1
    while True:
        batch = gh_get(
            "https://api.github.com/user/repos",
            params={"per_page": 100, "page": page,
                    "sort": "updated", "affiliation": "owner"}
        )
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos

# ── Main ─────────────────────────────────────────────────────
def main():
    if not TOKEN:
        print("[ERROR] GH_TOKEN not set. Export it first.")
        return

    # 1. Fetch counts
    user_data = gh_get(f"https://api.github.com/user")
    public_count  = user_data.get("public_repos", 0)
    private_count = user_data.get("owned_private_repos", 0)
    total_count   = public_count + private_count
    date_str      = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"Public:  {public_count}")
    print(f"Private: {private_count}")
    print(f"Total:   {total_count}")

    # 2. Fetch full repo list
    repos = fetch_all_repos()
    print(f"Fetched {len(repos)} repos from API")

    # 3. Build markdown rows
    rows = []
    for i, r in enumerate(repos, 1):
        name  = r["name"]
        url   = r["html_url"]
        desc  = (r.get("description") or "—")[:70].replace("|", "｜")
        lang  = r.get("language") or "—"
        date  = (r.get("updated_at") or "")[:10]
        vis   = "🌐 Public" if not r.get("private") else "🔒 Private"
        rows.append(f"| {i} | [{name}]({url}) | {desc} | {vis} | {lang} | {date} |")

    repo_table = "\n".join(rows)

    # 4. Build replacement blocks
    count_block = (
        f"<!-- REPO_COUNT_START -->\n"
        f"| Metric | Count |\n"
        f"|--------|-------|\n"
        f"| \ud83c\udf10 Public Repos | **{public_count}** |\n"
        f"| \ud83d\udd12 Private Repos | **{private_count}** |\n"
        f"| \ud83d\udce6 Total Repos | **{total_count}** |\n"
        f"<!-- REPO_COUNT_END -->\n\n"
        f"> \ud83d\udd50 *Last updated: {date_str} \u00b7 Auto-refreshes every 6 hours via GitHub Actions*"
    )

    list_block = (
        f"<!-- REPO_LIST_START -->\n"
        f"| # | Repository | Description | Type | Language | Updated |\n"
        f"|---|------------|-------------|------|----------|---------| \n"
        f"{repo_table}\n"
        f"<!-- REPO_LIST_END -->"
    )

    # 5. Patch README.md
    readme_path = "README.md"
    readme = open(readme_path, "r", encoding="utf-8").read()

    readme = re.sub(
        r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->\n\n> .*?Actions\*",
        count_block,
        readme,
        flags=re.DOTALL,
    )
    readme = re.sub(
        r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
        list_block,
        readme,
        flags=re.DOTALL,
    )

    open(readme_path, "w", encoding="utf-8").write(readme)
    print(f"README.md updated: {total_count} repos · {date_str}")

if __name__ == "__main__":
    main()
