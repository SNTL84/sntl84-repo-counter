#!/usr/bin/env python3
"""
SNTL84 · Repo Counter & README Auto-Updater
============================================
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

How counts work:
  PUBLIC repos  → GraphQL viewer.repositories(privacy: PUBLIC)
  PRIVATE count → GraphQL viewer.repositories(privacy: PRIVATE)
  GITHUB_TOKEN (built-in Actions token) has the `repo` scope by default
  when the workflow sets `permissions: contents: write` — this IS enough
  for GraphQL viewer queries scoped to the authenticated user.
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

GRAPHQL_URL = "https://api.github.com/graphql"


def graphql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        print(f"[ERROR] GraphQL {r.status_code}: {r.text[:300]}")
        r.raise_for_status()
    data = r.json()
    if "errors" in data:
        print(f"[ERROR] GraphQL errors: {data['errors']}")
        raise RuntimeError("GraphQL error")
    return data["data"]


def get_all_counts():
    """
    Use GraphQL viewer query — works with GITHUB_TOKEN in Actions
    when workflow has `permissions: contents: write`.
    Returns (public_count, private_count, public_repos_list).
    """
    query = """
    query($cursor: String) {
      viewer {
        login
        publicRepos: repositories(privacy: PUBLIC, first: 100, after: $cursor, ownerAffiliations: OWNER) {
          totalCount
          pageInfo { hasNextPage endCursor }
          nodes {
            name
            url
            description
            primaryLanguage { name }
            updatedAt
            isPrivate
          }
        }
        privateRepos: repositories(privacy: PRIVATE, ownerAffiliations: OWNER) {
          totalCount
        }
      }
    }
    """
    # First page
    data = graphql(query)
    viewer = data["viewer"]
    login = viewer["login"]
    print(f"[GraphQL] Authenticated as: {login}")

    public_total = viewer["publicRepos"]["totalCount"]
    private_total = viewer["privateRepos"]["totalCount"]
    public_repos = list(viewer["publicRepos"]["nodes"])
    page_info = viewer["publicRepos"]["pageInfo"]

    # Paginate public repos if needed
    while page_info["hasNextPage"]:
        page_query = """
        query($cursor: String) {
          viewer {
            publicRepos: repositories(privacy: PUBLIC, first: 100, after: $cursor, ownerAffiliations: OWNER) {
              pageInfo { hasNextPage endCursor }
              nodes {
                name
                url
                description
                primaryLanguage { name }
                updatedAt
                isPrivate
              }
            }
          }
        }
        """
        page_data = graphql(page_query, {"cursor": page_info["endCursor"]})
        batch = page_data["viewer"]["publicRepos"]
        public_repos.extend(batch["nodes"])
        page_info = batch["pageInfo"]

    print(f"[GraphQL] Public: {public_total}  Private: {private_total}")
    return public_total, private_total, public_repos


def main():
    if not TOKEN:
        print("[WARN] No token — cannot fetch counts.")
        return

    public_count, private_count, public_repos = get_all_counts()
    total_count = public_count + private_count
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"\nPublic:  {public_count}")
    print(f"Private: {private_count}")
    print(f"Total:   {total_count}\n")

    # Build repo list rows (public only, private not listed)
    rows = []
    for i, r in enumerate(public_repos, 1):
        name = r["name"]
        url  = r["url"]
        desc = (r.get("description") or "\u2014")[:90].replace("|", "\uff5c")
        lang = (r.get("primaryLanguage") or {}).get("name") or "\u2014"
        date = (r.get("updatedAt") or "")[:10]
        rows.append(f"| {i} | [{name}]({url}) | {desc} | \U0001f310 Public | {lang} | {date} |")

    if private_count > 0:
        label = f"{private_count} private repo{'s' if private_count != 1 else ''}"
        rows.append(f"| \u2014 | *{label}* | *Not listed \u2014 private* | \U0001f512 Private | \u2014 | \u2014 |")
    else:
        rows.append("| \u2014 | *Private repos* | *0 private repos* | \U0001f512 Private | \u2014 | \u2014 |")

    repo_table = "\n".join(rows)

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
