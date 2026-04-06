#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

Works with the built-in GITHUB_TOKEN (no PAT needed).
Fetches all repos via /user/repos (authenticated),
counts public + private, lists them, patches README.md.

Local usage:
  GH_TOKEN=ghp_yourPAT python3 scripts/count_repos.py
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
    """Paginate /user/repos to get ALL repos (public+private)."""
    repos, page = [], 1
    while True:
        batch = gh_get(
            "https://api.github.com/user/repos",
            params={"per_page": 100, "page": page,
                    "sort": "updated", "affiliation": "owner",
                    "visibility": "all"}
        )
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos

# ── Main ─────────────────────────────────────────────────────
def main():
    if not TOKEN:
        print("[ERROR] GH_TOKEN not set.")
        raise SystemExit(1)

    # 1. Fetch all repos (paginated)
    repos = fetch_all_repos()
    public_repos  = [r for r in repos if not r.get("private")]
    private_repos = [r for r in repos if r.get("private")]
    public_count  = len(public_repos)
    private_count = len(private_repos)
    total_count   = len(repos)
    date_str      = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"Public:  {public_count}")
    print(f"Private: {private_count}")
    print(f"Total:   {total_count}")

    # 2. Build markdown rows
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

    # 3. Build replacement blocks
    count_block = (
        "<!-- REPO_COUNT_START -->\n"
        "| Metric | Count |\n"
        "|--------|-------|\n"
        f"| \ud83c\udf10 Public Repos | **{public_count}** |\n"
        f"| \ud83d\udd12 Private Repos | **{private_count}** |\n"
        f"| \ud83d\udce6 Total Repos | **{total_count}** |\n"
        "<!-- REPO_COUNT_END -->\n\n"
        f"> \ud83d\udd50 *Last updated: {date_str} \u00b7 Auto-refreshes every 6 hours via GitHub Actions*"
    )

    list_block = (
        "<!-- REPO_LIST_START -->\n"
        "| # | Repository | Description | Type | Language | Updated |\n"
        "|---|------------|-------------|------|----------|---------|\n"
        f"{repo_table}\n"
        "<!-- REPO_LIST_END -->"
    )

    # 4. Patch README.md
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
