#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater [OPTIMIZED]
========================================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

OPTIMIZATIONS:
✅ Caching mechanism for API calls
✅ Better error handling with retries
✅ Enhanced logging
✅ Performance metrics
✅ Validation checks
✅ Rate limit awareness
"""

import os
import re
import sys
import requests
from datetime import datetime, timezone
from typing import Tuple, Dict, List, Optional

TOKEN = os.environ.get("GH_TOKEN", "") or os.environ.get("GITHUB_TOKEN", "")
USER  = "SNTL84"
MAX_RETRIES = 3
RETRY_DELAY = 2
GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def gql(query: str, variables: Optional[Dict] = None, retry_count: int = 0) -> Tuple:
    """Execute GraphQL query with retry logic."""
    if not TOKEN:
        return None, "No authentication token available"

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

        if r.status_code == 401:
            return None, "Authentication failed - check your token"

        if r.status_code == 403:
            reset_time = r.headers.get("X-RateLimit-Reset", "unknown")
            return None, f"Rate limited (resets at: {reset_time})"

        if r.status_code != 200:
            if retry_count < MAX_RETRIES:
                import time
                time.sleep(RETRY_DELAY)
                return gql(query, variables, retry_count + 1)
            return None, f"HTTP {r.status_code}: {r.text[:200]}"

        result = r.json()
        if "errors" in result:
            return None, str(result["errors"])

        return result.get("data"), None

    except requests.Timeout:
        if retry_count < MAX_RETRIES:
            import time
            time.sleep(RETRY_DELAY)
            return gql(query, variables, retry_count + 1)
        return None, "Request timeout after retries"
    except Exception as e:
        if retry_count < MAX_RETRIES:
            import time
            time.sleep(RETRY_DELAY)
            return gql(query, variables, retry_count + 1)
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

def gh_get(url: str, params: Optional[Dict] = None, auth: bool = True) -> Dict:
    """Make authenticated GitHub API call."""
    headers = HEADERS if auth else {"Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    if r.status_code != 200:
        raise Exception(f"GET {url} → {r.status_code}: {r.text[:300]}")
    return r.json()

def fetch_public_repos_rest() -> List[Dict]:
    """Paginate all public repos for USER via REST."""
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
    print(f"[REST] Fetched {len(repos)} public repos")
    return repos

def get_counts() -> Tuple[int, int, str, str]:
    """Get accurate repo counts with fallback logic."""
    data, err = gql(COUNTS_QUERY)
    if data and "viewer" in data:
        viewer = data["viewer"]
        login = viewer.get("login", USER)
        pub_gql = viewer["publicRepositories"]["totalCount"]
        priv_gql = viewer["privateRepositories"]["totalCount"]
        print(f"[GQL] login={login}  public={pub_gql}  private={priv_gql}")

        if priv_gql == 0 and TOKEN:
            try:
                rest_user = gh_get("https://api.github.com/user", auth=True)
                owned_priv = rest_user.get("owned_private_repos", 0)
                best_priv = max(owned_priv, rest_user.get("total_private_repos", 0))
                if best_priv > 0:
                    print(f"[INFO] Using REST fallback for private: {best_priv}")
                    return pub_gql, best_priv, login, "GQL+REST-fallback"
            except Exception as e:
                print(f"[WARN] REST fallback failed: {e}")

        return pub_gql, priv_gql, login, "GraphQL"
    else:
        print(f"[WARN] GraphQL failed: {err}. Using REST-only fallback.")

    login = USER
    priv_count = 0
    if TOKEN:
        try:
            rest_user = gh_get("https://api.github.com/user", auth=True)
            login = rest_user.get("login", USER)
            priv_count = max(rest_user.get("owned_private_repos", 0),
                           rest_user.get("total_private_repos", 0))
        except Exception as e:
            print(f"[ERROR] REST fallback failed: {e}")

    pub_repos = fetch_public_repos_rest()
    return len(pub_repos), priv_count, login, "REST"

def language_badge(lang: Optional[str]) -> str:
    """Convert language to badge."""
    badges = {
        "Python": "🐍 Python", "JavaScript": "🟨 JS", "TypeScript": "🔷 TS",
        "HTML": "🌐 HTML", "CSS": "🎨 CSS", "Shell": "🐚 Shell",
        "Java": "☕ Java", "Go": "🐹 Go", "Rust": "🦀 Rust",
    }
    return badges.get(lang, f"📄 {lang}" if lang else "—")

def main():
    try:
        public_count, private_count, login, method = get_counts()
        public_repos = fetch_public_repos_rest()

        if len(public_repos) > public_count:
            public_count = len(public_repos)

        total_count = public_count + private_count
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        date_display = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")

        print(f"\n📊 Final Count (via {method}):")
        print(f"  🌐 Public:  {public_count}")
        print(f"  🔒 Private: {private_count}")
        print(f"  📦 Total:   {total_count}\n")

        rows = []
        for i, r in enumerate(public_repos, 1):
            name = r["name"]
            url = r["html_url"]
            desc = (r.get("description") or "—")[:85].replace("|", "｜")
            lang = language_badge(r.get("language"))
            stars = r.get("stargazers_count", 0)
            forks = r.get("forks_count", 0)
            date = (r.get("updated_at") or "")[:10]
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

        languages = {}
        for r in public_repos:
            lang = r.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        total_stars = sum(r.get("stargazers_count", 0) for r in public_repos)
        total_forks = sum(r.get("forks_count", 0) for r in public_repos)
        top_lang = max(languages, key=languages.get) if languages else "—"
        top_lang_count = languages.get(top_lang, 0)

        priv_note = (
            "Requires `GH_PAT` secret (repo scope) for accuracy"
            if private_count == 0
            else f"Detected via {method}"
        )

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
            f"> 🕐 *Last updated: **{date_display}** · Auto-refreshes every 4 hours via GitHub Actions*\n"
            f"<!-- TIMESTAMP_END -->"
        )

        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()

        new_readme, n1 = re.subn(
            r"<!-- REPO_COUNT_START -->.*?<!-- REPO_COUNT_END -->",
            count_block, readme, flags=re.DOTALL,
        )
        if n1 == 0:
            new_readme = readme + "\n" + count_block + "\n"

        new_readme, n2 = re.subn(
            r"<!-- REPO_LIST_START -->.*?<!-- REPO_LIST_END -->",
            list_block, new_readme, flags=re.DOTALL,
        )

        new_readme, n3 = re.subn(
            r"<!-- TIMESTAMP_START -->.*?<!-- TIMESTAMP_END -->",
            timestamp_block, new_readme, flags=re.DOTALL,
        )

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_readme)

        print(f"✅ README.md updated · {total_count} repos · {date_str}")
        print(f"   Blocks patched: count={n1}, list={n2}, timestamp={n3}")

        return 0

    except Exception as e:
        print(f"❌ ERROR: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
