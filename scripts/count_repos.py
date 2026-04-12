#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

How counts work:
  PUBLIC count  → /users/SNTL84 (public API, always works, no auth)
  PRIVATE count → GH_PAT with `repo` scope (add as GitHub Secret `GH_PAT`)
                  Falls back to 0 if not set — adds a warning in README
  TOTAL         → public + private

Local usage:
  GH_PAT=ghp_yourPAT python3 scripts/count_repos.py
"""

import os
import re
import sys
import requests
from datetime import datetime, timezone

TOKEN   = os.environ.get("GH_TOKEN", "")   # built-in GITHUB_TOKEN (no private access)
GH_PAT  = os.environ.get("GH_PAT", "")     # PAT with `repo` scope for private count
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
} if GH_PAT else None


def gh_get(url, params=None, hdrs=None):
    hdrs = hdrs or HEADERS
    r = requests.get(url, headers=hdrs, params=params, timeout=15)
    if r.status_code != 200:
        print(f"[ERROR] GET {url} → {r.status_code}: {r.text[:200]}")
        r.raise_for_status()
    return r.json()


def fetch_public_repos():
    """Fetch all public repos via /users/{USER}/repos (no auth required)."""
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


def get_private_count():
    """
    Get accurate private repo count via GH_PAT with `repo` scope.
    The /user endpoint returns `owned_private_repos` which is the
    true count of private repos owned by the authenticated user.
    Returns (count: int, pat_available: bool).
    """
    if not GH_PAT:
        print("[WARN] GH_PAT not set — private count = 0. Add GH_PAT secret (repo scope) for accurate count.")
        return 0, False

    try:
        data = gh_get("https://api.github.com/user", hdrs=PAT_HEADERS)
        # Validate we got the right user
        login = data.get("login", "")
        if login.lower() != USER.lower():
            print(f"[WARN] PAT belongs to '{login}', expected '{USER}'. Private count may be inaccurate.")
        owned_private = data.get("owned_private_repos", 0)
        total_private = data.get("total_private_repos", 0)  # includes org repos
        pub = data.get("public_repos", 0)
        print(f"[PAT] login={login} public={pub} owned_private={owned_private} total_private={total_private}")
        # Use owned_private_repos — this is repos the user OWNS (not org-shared)
        return owned_private, True
    except Exception as e:
        print(f"[ERROR] PAT fetch failed: {e} — defaulting private count to 0")
        return 0, False


def main():
    # ── 1. Counts ─────────────────────────────────────────────────────────────
    public_repos   = fetch_public_repos()
    public_count   = len(public_repos)
    private_count, pat_ok = get_private_count()
    total_count    = public_count + private_count
    date_str       = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"Public:  {public_count}")
    print(f"Private: {private_count} {'(via PAT)' if pat_ok else '(GH_PAT missing — may be inaccurate)'}")
    print(f"Total:   {total_count}")

    # ── 2. Build repo list rows ────────────────────────────────────────────────
    rows = []
    for i, r in enumerate(public_repos, 1):
        name = r["name"]
        url  = r["html_url"]
        desc = (r.get("description") or "—")[:90].replace("|", "｜")
        lang = r.get("language") or "—"
        date = (r.get("updated_at") or "")[:10]
        rows.append(f"| {i} | [{name}]({url}) | {desc} | 🌐 Public | {lang} | {date} |")

    if private_count > 0:
        rows.append(
            f"| — | *{private_count} private repo{'s' if private_count > 1 else ''}* "
            f"| *Not listed for privacy* | 🔒 Private | — | — |"
        )
    elif not pat_ok:
        rows.append(
            "| — | *Private repos* | ⚠️ GH_PAT not set — private count unavailable | 🔒 Private | — | — |"
        )

    repo_table = "\n".join(rows)

    # ── 3. Warning note if PAT missing ────────────────────────────────────────
    pat_note = (
        "" if pat_ok else
        "\n> ⚠️ **Private count is unavailable.** Add a `GH_PAT` secret (with `repo` scope) in "
        "[Settings → Secrets](https://github.com/SNTL84/sntl84-repo-counter/settings/secrets/actions) "
        "to display accurate private repo count."
    )

    # ── 4. Replacement blocks ─────────────────────────────────────────────────
    count_block = (
        "<!-- REPO_COUNT_START -->\n"
        "| Metric | Count |\n"
        "|--------|-------|\n"
        f"| 🌐 Public Repos | **{public_count}** |\n"
        f"| 🔒 Private Repos | **{private_count}**{'' if pat_ok else ' ⚠️'} |\n"
        f"| 📦 Total Repos | **{total_count}** |\n"
        "<!-- REPO_COUNT_END -->\n\n"
        f"> 🕐 *Last updated: {date_str} · Auto-refreshes every 6 hours via GitHub Actions*"
        f"{pat_note}"
    )
    list_block = (
        "<!-- REPO_LIST_START -->\n"
        "| # | Repository | Description | Type | Language | Updated |\n"
        "|---|------------|-------------|------|----------|---------|\n"
        f"{repo_table}\n"
        "<!-- REPO_LIST_END -->"
    )

    # ── 5. Patch README ────────────────────────────────────────────────────────
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    # Replace count block
    new_readme, n1 = re.subn(
        r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->\n\n> .*?(?=\n[^>]|\Z)",
        count_block,
        readme,
        flags=re.DOTALL,
    )
    if n1 == 0:
        print("[WARN] REPO_COUNT markers not found in README — skipping count block update.")
        new_readme = readme

    # Replace list block
    new_readme, n2 = re.subn(
        r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
        list_block,
        new_readme,
        flags=re.DOTALL,
    )
    if n2 == 0:
        print("[WARN] REPO_LIST markers not found in README — skipping list block update.")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"README.md updated — {total_count} repos · {date_str}")

    # Exit with error if PAT is missing so workflow logs are visible
    if not pat_ok:
        print("\n[ACTION REQUIRED] Set GH_PAT secret for accurate private repo count.")
        # Don't fail the workflow — just warn


if __name__ == "__main__":
    main()
