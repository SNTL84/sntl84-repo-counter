#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

How counts work:
  PUBLIC repos  → /users/SNTL84/repos (public REST, no auth needed)
  PRIVATE count → /user REST endpoint with GITHUB_TOKEN
                   GITHUB_TOKEN in Actions returns owned_private_repos
                   accurately for the authenticated user.
  If GH_PAT is set (classic token, repo scope), it is used instead
  for maximum accuracy.
  TOTAL         → public + private

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
    """Paginate all public repos for USER via unauthenticated public API."""
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
    Call /user with GITHUB_TOKEN to get owned_private_repos.
    GITHUB_TOKEN in Actions is authenticated as the repo owner (SNTL84)
    and DOES return the correct owned_private_repos count.
    Returns (private_count, login).
    """
    if not TOKEN:
        print("[WARN] No token — private count will be 0.")
        return 0, "unknown"
    try:
        data = gh_get("https://api.github.com/user", auth=True)
        login          = data.get("login", "unknown")
        private_count  = data.get("owned_private_repos", 0)
        total_private  = data.get("total_private_repos", 0)
        print(f"[REST /user] login={login}")
        print(f"[REST /user] owned_private_repos={private_count}  total_private_repos={total_private}")
        return private_count, login
    except Exception as e:
        print(f"[ERROR] /user fetch failed: {e}")
        return 0, "unknown"


def main():
    # 1. Fetch counts
    public_repos   = fetch_public_repos()
    public_count   = len(public_repos)
    private_count, login = get_private_count()
    total_count    = public_count + private_count
    date_str       = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"\nPublic:  {public_count}")
    print(f"Private: {private_count}")
    print(f"Total:   {total_count}\n")

    # 2. Build repo list rows
    rows = []
    for i, r in enumerate(public_repos, 1):
        name = r["name"]
        url  = r["html_url"]
        desc = (r.get("description") or "\u2014")[:90].replace("|", "\uff5c")
        lang = r.get("language") or "\u2014"
        date = (r.get("updated_at") or "")[:10]
        rows.append(f"| {i} | [{name}]({url}) | {desc} | \U0001f310 Public | {lang} | {date} |")

    if private_count > 0:
        label = f"{private_count} private repo{'s' if private_count != 1 else ''}"
        rows.append(f"| \u2014 | *{label}* | *Not listed \u2014 private* | \U0001f512 Private | \u2014 | \u2014 |")
    else:
        rows.append("| \u2014 | *Private repos* | *0 private repos* | \U0001f512 Private | \u2014 | \u2014 |")

    repo_table = "\n".join(rows)

    # 3. Build README blocks
    count_block = (
        "<!-- REPO_COUNT_START -->\n"
        "| Metric | Count |\n"
        "|--------|-------|\n"
        f"| \U0001f310 Public Repos  | **{public_count}** |\n"
        f"| \U0001f512 Private Repos | **{private_count}** |\n"
        f"| \U0001f4e6 Total Repos   | **{total_count}** |\n"
        "<!-- REPO_COUNT_END -->\n\n"
        f"> \U0001f550 *Last updated: {date_str} \u00b7 Auto-refreshes every 6 hours via GitHub Actions*"
    )

    list_block = (
        "<!-- REPO_LIST_START -->\n"
        "| # | Repository | Description | Type | Language | Updated |\n"
        "|---|------------|-------------|------|----------|---------|\n"
        f"{repo_table}\n"
        "<!-- REPO_LIST_END -->"
    )

    # 4. Patch README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    new_readme, n1 = re.subn(
        r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->\n\n> .*?(?=\n[^>]|\Z)",
        count_block,
        readme,
        flags=re.DOTALL,
    )
    if n1 == 0:
        print("[WARN] REPO_COUNT markers not found.")
        new_readme = readme

    new_readme, n2 = re.subn(
        r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
        list_block,
        new_readme,
        flags=re.DOTALL,
    )
    if n2 == 0:
        print("[WARN] REPO_LIST markers not found.")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"\u2705 README.md updated \u2014 {total_count} total repos \u00b7 {date_str}")


if __name__ == "__main__":
    main()
