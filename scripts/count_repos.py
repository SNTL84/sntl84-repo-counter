#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

How counts work:
  PUBLIC count  → /users/SNTL84 (public API, always works, no auth)
  PRIVATE count → env var GH_PAT_PRIVATE_COUNT (set as GitHub Secret)
                  OR env var PRIVATE_REPO_COUNT (fallback integer)
                  OR 0 if neither is set
  TOTAL         → public + private

Public repo LIST is fetched via /users/SNTL84/repos (always public).

To unlock private count:
  1. Create a PAT with repo scope
  2. Add secret GH_PAT to this repo (Settings > Secrets)
  3. The workflow will use it automatically

Local:
  GH_TOKEN=ghp_yourPAT python3 scripts/count_repos.py
"""

import os
import re
import requests
from datetime import datetime, timezone

TOKEN   = os.environ.get("GH_TOKEN", "")   # built-in GITHUB_TOKEN or PAT
GH_PAT  = os.environ.get("GH_PAT", "")     # optional PAT with repo scope
USER    = "SNTL84"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
PAT_HEADERS = {
    "Authorization": f"Bearer {GH_PAT}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
} if GH_PAT else HEADERS

def gh_get(url, params=None, hdrs=None):
    r = requests.get(url, headers=hdrs or HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def fetch_public_repos():
    repos, page = [], 1
    while True:
        batch = gh_get(
            f"https://api.github.com/users/{USER}/repos",
            params={"per_page": 100, "page": page, "sort": "updated"},
        )
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos

def get_private_count():
    """Try to get private count via PAT. Returns int or None."""
    if GH_PAT:
        try:
            data = gh_get("https://api.github.com/user", hdrs=PAT_HEADERS)
            pub  = data.get("public_repos", 0)
            owned = data.get("owned_private_repos", 0)
            print(f"PAT auth — public={pub}, private={owned}")
            return owned
        except Exception as e:
            print(f"PAT fetch failed: {e}")
    # Try PRIVATE_REPO_COUNT env var (set manually in workflow)
    try:
        return int(os.environ.get("PRIVATE_REPO_COUNT", "0"))
    except Exception:
        return 0

def main():
    # 1. Public repos (always works)
    public_repos  = fetch_public_repos()
    public_count  = len(public_repos)

    # 2. Private count
    private_count = get_private_count()
    total_count   = public_count + private_count
    date_str      = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"Public:  {public_count}")
    print(f"Private: {private_count}")
    print(f"Total:   {total_count}")

    # 3. Build markdown rows
    rows = []
    for i, r in enumerate(public_repos, 1):
        name = r["name"]
        url  = r["html_url"]
        desc = (r.get("description") or "—")[:70].replace("|", "｜")
        lang = r.get("language") or "—"
        date = (r.get("updated_at") or "")[:10]
        rows.append(f"| {i} | [{name}]({url}) | {desc} | 🌐 Public | {lang} | {date} |")
    if private_count > 0:
        rows.append(f"| — | *{private_count} private repos* | *Not listed for privacy* | 🔒 Private | — | — |")

    repo_table = "\n".join(rows)

    # 4. Replacement blocks
    count_block = (
        "<!-- REPO_COUNT_START -->\n"
        "| Metric | Count |\n"
        "|--------|-------|\n"
        f"| 🌐 Public Repos | **{public_count}** |\n"
        f"| 🔒 Private Repos | **{private_count}** |\n"
        f"| 📦 Total Repos | **{total_count}** |\n"
        "<!-- REPO_COUNT_END -->\n\n"
        f"> 🕐 *Last updated: {date_str} \u00b7 Auto-refreshes every 6 hours via GitHub Actions*"
    )
    list_block = (
        "<!-- REPO_LIST_START -->\n"
        "| # | Repository | Description | Type | Language | Updated |\n"
        "|---|------------|-------------|------|----------|---------|\n"
        f"{repo_table}\n"
        "<!-- REPO_LIST_END -->"
    )

    # 5. Patch README
    readme = open("README.md", "r", encoding="utf-8").read()
    readme = re.sub(
        r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->\n\n> .*?Actions\*",
        count_block, readme, flags=re.DOTALL)
    readme = re.sub(
        r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
        list_block, readme, flags=re.DOTALL)
    open("README.md", "w", encoding="utf-8").write(readme)
    print(f"README.md updated — {total_count} repos · {date_str}")

if __name__ == "__main__":
    main()
