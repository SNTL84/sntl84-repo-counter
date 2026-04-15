#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

Accuracy notes:
  PUBLIC  → GraphQL viewer.repositories(privacy:PUBLIC) — most accurate count
            Falls back to paginated REST /users/SNTL84/repos if GraphQL fails
  PRIVATE → GraphQL viewer.repositories(privacy:PRIVATE) — requires GH_PAT (repo scope)
            Falls back to REST /user → owned_private_repos
            GITHUB_TOKEN (default Actions token) returns 0 for private — set GH_PAT secret!
  TOTAL   → public + private (both via same GraphQL call)

  To fix private count:
    1. GitHub → Settings → Developer Settings → Personal Access Tokens → Classic
    2. Generate token with 'repo' scope
    3. This repo → Settings → Secrets → Actions → New secret: GH_PAT
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

GRAPHQL_URL = "https://api.github.com/graphql"


# ─── GraphQL helpers ──────────────────────────────────────────────────────────

def gql(query: str, variables: dict = None):
    """Execute a GraphQL query. Returns (data_dict, error_message)."""
    if not TOKEN:
        return None, "No token available"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    try:
        r = requests.post(
            GRAPHQL_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=20,
        )
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:200]}"
        result = r.json()
        if "errors" in result:
            return None, str(result["errors"])
        return result.get("data"), None
    except Exception as e:
        return None, str(e)


COUNTS_QUERY = """
query GetRepoCounts {
  viewer {
    login
    publicRepositories: repositories(privacy: PUBLIC, ownerAffiliations: OWNER) {
      totalCount
    }
    privateRepositories: repositories(privacy: PRIVATE, ownerAffiliations: OWNER) {
      totalCount
    }
  }
}
"""


# ─── REST helpers ─────────────────────────────────────────────────────────────

def gh_get(url, params=None, auth=True):
    headers = HEADERS if auth else {"Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    if r.status_code != 200:
        print(f"[ERROR] GET {url} → {r.status_code}: {r.text[:300]}")
        r.raise_for_status()
    return r.json()


def fetch_public_repos_rest():
    """Paginate ALL public repos for USER via REST (for listing table)."""
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


# ─── Count logic ──────────────────────────────────────────────────────────────

def get_counts():
    """
    Returns (public_count, private_count, login, method_used).

    Strategy:
      1. Try GraphQL viewer query — most accurate, single call
         Works for both public and private IF token has 'repo' scope (GH_PAT)
         With GITHUB_TOKEN: public count is accurate, private will return 0
      2. Fall back to REST /user for private if GraphQL private = 0 but REST shows more
    """
    # ── GraphQL attempt ──────────────────────────────────────────────────────
    data, err = gql(COUNTS_QUERY)
    if data and "viewer" in data:
        viewer       = data["viewer"]
        login        = viewer.get("login", USER)
        pub_gql      = viewer["publicRepositories"]["totalCount"]
        priv_gql     = viewer["privateRepositories"]["totalCount"]
        print(f"[GQL] login={login}  public={pub_gql}  private={priv_gql}")

        # If private is 0, double-check via REST /user in case token lacks scope
        if priv_gql == 0 and TOKEN:
            try:
                rest_user     = gh_get("https://api.github.com/user", auth=True)
                owned_priv    = rest_user.get("owned_private_repos", 0)
                total_priv    = rest_user.get("total_private_repos", 0)
                print(f"[REST /user] owned_private_repos={owned_priv}  total_private_repos={total_priv}")
                # Use the larger of the two as the best estimate
                best_priv = max(owned_priv, total_priv)
                if best_priv > 0:
                    print(f"[INFO] GraphQL returned 0 private — using REST fallback: {best_priv}")
                    print("[HINT] Set GH_PAT secret (repo scope) for accurate GraphQL private count.")
                    return pub_gql, best_priv, login, "GQL+REST-fallback"
            except Exception as e:
                print(f"[WARN] REST /user fallback failed: {e}")

        return pub_gql, priv_gql, login, "GraphQL"
    else:
        print(f"[WARN] GraphQL failed: {err}. Falling back to REST.")

    # ── REST-only fallback ───────────────────────────────────────────────────
    login = USER
    if TOKEN:
        try:
            rest_user     = gh_get("https://api.github.com/user", auth=True)
            login         = rest_user.get("login", USER)
            owned_priv    = rest_user.get("owned_private_repos", 0)
            total_priv    = rest_user.get("total_private_repos", 0)
            priv_count    = max(owned_priv, total_priv)
            print(f"[REST /user] login={login}  owned_private={owned_priv}  total_private={total_priv}")
        except Exception as e:
            print(f"[ERROR] REST /user failed: {e}")
            priv_count = 0
    else:
        print("[WARN] No token — private count will be 0")
        priv_count = 0

    # Public count from REST
    pub_repos  = fetch_public_repos_rest()
    pub_count  = len(pub_repos)
    return pub_count, priv_count, login, "REST"


# ─── Utilities ────────────────────────────────────────────────────────────────

def language_badge(lang):
    badges = {
        "Python": "🐍 Python", "JavaScript": "🟨 JS", "TypeScript": "🔷 TS",
        "HTML": "🌐 HTML", "CSS": "🎨 CSS", "Shell": "🐚 Shell",
        "Java": "☕ Java", "Go": "🐹 Go", "Rust": "🦀 Rust",
        "Ruby": "💎 Ruby", "PHP": "🐘 PHP", "C++": "⚙️ C++",
    }
    return badges.get(lang, f"📄 {lang}" if lang else "—")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # 1. Fetch accurate counts
    public_count, private_count, login, method = get_counts()

    # For the repo listing table we always need the REST public list
    public_repos = fetch_public_repos_rest()

    # Reconcile: if GraphQL gave a different public count, trust the larger
    if len(public_repos) > public_count:
        print(f"[INFO] REST listed {len(public_repos)} repos vs GQL {public_count} — using REST count for table accuracy")
        public_count = len(public_repos)

    total_count   = public_count + private_count
    date_str      = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    date_display  = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")

    print(f"\n📊 Final Count (via {method}):")
    print(f"  🌐 Public:  {public_count}")
    print(f"  🔒 Private: {private_count}")
    print(f"  📦 Total:   {total_count}\n")

    # 2. Build repo list rows
    rows = []
    for i, r in enumerate(public_repos, 1):
        name     = r["name"]
        url      = r["html_url"]
        desc     = (r.get("description") or "—")[:85].replace("|", "｜")
        lang     = language_badge(r.get("language"))
        stars    = r.get("stargazers_count", 0)
        forks    = r.get("forks_count", 0)
        date     = (r.get("updated_at") or "")[:10]
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
        rows.append(
            "| — | *Private repos* | *0 detected — add GH_PAT secret (repo scope) if you have private repos* | 🔒 Private | — | — | — |"
        )

    repo_table = "\n".join(rows)

    # 3. Stats
    languages    = {}
    for r in public_repos:
        lang = r.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    total_stars  = sum(r.get("stargazers_count", 0) for r in public_repos)
    total_forks  = sum(r.get("forks_count", 0) for r in public_repos)
    top_lang     = max(languages, key=languages.get) if languages else "—"
    top_lang_count = languages.get(top_lang, 0)

    # Private count note for README
    priv_note = (
        "Requires `GH_PAT` secret (repo scope) for accuracy"
        if private_count == 0
        else f"Detected via {method}"
    )

    # 4. Build README blocks
    count_block = (
        "<!-- REPO_COUNT_START -->\n"
        "| Metric | Count | Details |\n"
        "|--------|-------|---------|\n"
        f"| 🌐 Public Repos  | **{public_count}** | All public repositories |\n"
        f"| 🔒 Private Repos | **{private_count}** | {priv_note} |\n"
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

    # 5. Patch README
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
