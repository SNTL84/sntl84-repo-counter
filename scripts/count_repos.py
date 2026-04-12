#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

How counts work:
  PUBLIC repos  → fetched via /users/SNTL84/repos (paginated, no auth needed)
  PRIVATE count → /user endpoint using GITHUB_TOKEN (always present in Actions)
                  GITHUB_TOKEN is authenticated as SNTL84, so it CAN see private counts.
                  GH_PAT secret is NOT required.
  TOTAL         → public + private

Local usage:
  GH_TOKEN=ghp_yourToken python3 scripts/count_repos.py
"""

import os
import re
import requests
from datetime import datetime, timezone

# GITHUB_TOKEN is automatically injected by GitHub Actions — always present
TOKEN = os.environ.get("GH_TOKEN", "") or os.environ.get("GITHUB_TOKEN", "")
USER  = "SNTL84"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def gh_get(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    if r.status_code != 200:
        print(f"[ERROR] GET {url} → {r.status_code}: {r.text[:300]}")
        r.raise_for_status()
    return r.json()


def fetch_public_repos():
    """Paginate all public repos for USER."""
    repos, page = [], 1
    while True:
        batch = gh_get(
            f"https://api.github.com/users/{USER}/repos",
            params={"per_page": 100, "page": page, "sort": "updated"},
        )
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def get_counts_from_token():
    """
    Call /user with GITHUB_TOKEN.
    In GitHub Actions, GITHUB_TOKEN is scoped to the repo owner (SNTL84),
    so this returns accurate public + private counts directly.
    Returns (public_count, private_count, token_authed: bool).
    """
    if not TOKEN:
        print("[WARN] No token available — private count will be 0.")
        return None, 0, False

    try:
        data = gh_get("https://api.github.com/user")
        login         = data.get("login", "unknown")
        public_count  = data.get("public_repos", 0)
        private_count = data.get("owned_private_repos", 0)
        print(f"[TOKEN] Authenticated as: {login}")
        print(f"[TOKEN] public_repos={public_count}  owned_private_repos={private_count}")
        if login.lower() != USER.lower():
            print(f"[WARN] Token owner '{login}' != expected '{USER}' — counts may differ.")
        return public_count, private_count, True
    except Exception as e:
        print(f"[ERROR] /user fetch failed: {e}")
        return None, 0, False


def main():
    # ── 1. Fetch data ─────────────────────────────────────────────────────────
    public_repos = fetch_public_repos()
    public_from_list = len(public_repos)

    api_public, private_count, token_ok = get_counts_from_token()

    # Use API-reported public count if token is authenticated (more authoritative),
    # fall back to pagination count
    public_count = api_public if (token_ok and api_public is not None) else public_from_list
    total_count  = public_count + private_count
    date_str     = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"\nPublic:  {public_count}")
    print(f"Private: {private_count}")
    print(f"Total:   {total_count}\n")

    # ── 2. Build repo list rows ───────────────────────────────────────────────
    rows = []
    for i, r in enumerate(public_repos, 1):
        name = r["name"]
        url  = r["html_url"]
        desc = (r.get("description") or "—")[:90].replace("|", "｜")
        lang = r.get("language") or "—"
        date = (r.get("updated_at") or "")[:10]
        rows.append(f"| {i} | [{name}]({url}) | {desc} | 🌐 Public | {lang} | {date} |")

    if private_count > 0:
        label = f"{private_count} private repo{'s' if private_count != 1 else ''}"
        rows.append(f"| — | *{label}* | *Not listed — private* | 🔒 Private | — | — |")
    else:
        rows.append("| — | *Private repos* | *0 private repos* | 🔒 Private | — | — |")

    repo_table = "\n".join(rows)

    # ── 3. Build README blocks ────────────────────────────────────────────────
    count_block = (
        "<!-- REPO_COUNT_START -->\n"
        "| Metric | Count |\n"
        "|--------|-------|\n"
        f"| 🌐 Public Repos | **{public_count}** |\n"
        f"| 🔒 Private Repos | **{private_count}** |\n"
        f"| 📦 Total Repos | **{total_count}** |\n"
        "<!-- REPO_COUNT_END -->\n\n"
        f"> 🕐 *Last updated: {date_str} · Auto-refreshes every 6 hours via GitHub Actions*"
    )
    list_block = (
        "<!-- REPO_LIST_START -->\n"
        "| # | Repository | Description | Type | Language | Updated |\n"
        "|---|------------|-------------|------|----------|---------|\n"
        f"{repo_table}\n"
        "<!-- REPO_LIST_END -->"
    )

    # ── 4. Patch README ───────────────────────────────────────────────────────
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    new_readme, n1 = re.subn(
        r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->\n\n> .*?(?=\n[^>]|\Z)",
        count_block,
        readme,
        flags=re.DOTALL,
    )
    if n1 == 0:
        print("[WARN] REPO_COUNT markers not found — skipping count block.")
        new_readme = readme

    new_readme, n2 = re.subn(
        r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
        list_block,
        new_readme,
        flags=re.DOTALL,
    )
    if n2 == 0:
        print("[WARN] REPO_LIST markers not found — skipping list block.")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"✅ README.md updated — {total_count} total repos · {date_str}")


if __name__ == "__main__":
    main()
