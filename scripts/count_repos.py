#!/usr/bin/env python3
"""
SNTL84 Repo Counter — Local runner
Milan · SNTL 84 · desidevloper.com
I Automate What's Costing You Money.

Usage:
    GH_TOKEN=your_token python3 scripts/count_repos.py
"""

import os, json, re
from urllib import request, error

TOKEN = os.environ.get("GH_TOKEN", "")
USER  = "SNTL84"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def gh_get(url):
    req = request.Request(url, headers=HEADERS)
    with request.urlopen(req) as r:
        return json.loads(r.read())

def main():
    # Public count
    user_data   = gh_get(f"https://api.github.com/users/{USER}")
    public      = user_data["public_repos"]

    # Private count (requires auth)
    auth_data   = gh_get("https://api.github.com/user")
    private     = auth_data.get("owned_private_repos", 0)
    total       = public + private

    # Repo list
    repos       = gh_get(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated")

    print(f"\n{'='*50}")
    print(f"  SNTL84 · Milan · desidevloper.com")
    print(f"  Repository Counter")
    print(f"{'='*50}")
    print(f"  🌐 Public  : {public}")
    print(f"  🔒 Private : {private}")
    print(f"  📦 Total   : {total}")
    print(f"{'='*50}\n")
    print(f"  {'#':<4} {'Name':<45} {'Lang':<15} {'Updated'}")
    print(f"  {'-'*80}")
    for i, r in enumerate(repos, 1):
        name = r['name']
        lang = (r.get('language') or '—')[:14]
        date = (r.get('updated_at') or '')[:10]
        print(f"  {i:<4} {name:<45} {lang:<15} {date}")
    print()

if __name__ == "__main__":
    main()
