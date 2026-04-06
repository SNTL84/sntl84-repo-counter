#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

Strategy (works with built-in GITHUB_TOKEN on a PUBLIC repo):
  - Public repos: fetched via /users/SNTL84/repos (no special auth)
  - Public + private count: from /users/SNTL84 public field
    + GraphQL viewer.repositories.totalCount for total
  - Falls back gracefully if any endpoint is 403

Local usage:
  GH_TOKEN=ghp_yourPAT python3 scripts/count_repos.py
"""

import os
import re
import requests
from datetime import datetime, timezone

TOKEN = os.environ.get("GH_TOKEN", "")
USER  = "SNTL84"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def gh_get(url, params=None, headers=None):
    h = headers or HEADERS
    r = requests.get(url, headers=h, params=params)
    r.raise_for_status()
    return r.json()

def get_total_via_graphql():
    """Use GraphQL to get total repo count (public+private). Returns None on failure."""
    query = '{viewer{repositories(affiliations:OWNER){totalCount}}}'
    try:
        r = requests.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers={"Authorization": f"Bearer {TOKEN}",
                     "Content-Type": "application/json"}
        )
        data = r.json()
        return data["data"]["viewer"]["repositories"]["totalCount"]
    except Exception as e:
        print(f"GraphQL fallback failed: {e}")
        return None

def fetch_public_repos():
    """Paginate /users/SNTL84/repos — always public, no auth needed."""
    repos, page = [], 1
    while True:
        batch = gh_get(
            f"https://api.github.com/users/{USER}/repos",
            params={"per_page": 100, "page": page, "sort": "updated"},
            headers=HEADERS
        )
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos

def main():
    # 1. Public repo list (always accessible)
    public_repos = fetch_public_repos()
    public_count  = len(public_repos)

    # 2. Total count via GraphQL (works with GITHUB_TOKEN on same-owner repo)
    total_count = get_total_via_graphql()
    if total_count is None:
        # Fallback: use public_repos field from /users/{user}
        user_data = gh_get(f"https://api.github.com/users/{USER}")
        total_count = user_data.get("public_repos", public_count)
        print("[INFO] Using public_repos fallback for total count")

    private_count = max(0, total_count - public_count)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"Public:  {public_count}")
    print(f"Private: {private_count}")
    print(f"Total:   {total_count}")
    print(f"Date:    {date_str}")

    # 3. Build markdown rows (public repos only — private repos hidden for privacy)
    rows = []
    for i, r in enumerate(public_repos, 1):
        name  = r["name"]
        url   = r["html_url"]
        desc  = (r.get("description") or "—")[:70].replace("|", "｜")
        lang  = r.get("language") or "—"
        date  = (r.get("updated_at") or "")[:10]
        rows.append(f"| {i} | [{name}]({url}) | {desc} | 🌐 Public | {lang} | {date} |")

    # Add private repos note
    if private_count > 0:
        rows.append(f"| — | *{private_count} private repos* | *Hidden for privacy* | 🔒 Private | — | — |")

    repo_table = "\n".join(rows)

    # 4. Build replacement blocks
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

    # 5. Patch README.md
    readme = open("README.md", "r", encoding="utf-8").read()
    readme = re.sub(
        r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->\n\n> .*?Actions\*",
        count_block, readme, flags=re.DOTALL)
    readme = re.sub(
        r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
        list_block, readme, flags=re.DOTALL)
    open("README.md", "w", encoding="utf-8").write(readme)
    print(f"README.md updated: {total_count} repos")

if __name__ == "__main__":
    main()
