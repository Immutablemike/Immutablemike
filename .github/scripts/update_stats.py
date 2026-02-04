#!/usr/bin/env python3
"""
Generate real GitHub stats using HTML comment markers for safe replacement
"""

import os
import re
import sys
from datetime import datetime, timedelta
from github import Github


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not found!")
        sys.exit(1)

    g = Github(token)
    user = g.get_user()
    print(f"Fetching stats for {user.login}...")

    repos = list(user.get_repos(visibility="all"))
    total_repos = len(repos)
    public_repos = len([r for r in repos if not r.private])
    private_repos = len([r for r in repos if r.private])

    since = datetime.now() - timedelta(days=30)
    total_commits = 0
    total_prs = 0
    languages = {}

    for i, repo in enumerate(repos, 1):
        try:
            print(f"  [{i}/{total_repos}] {repo.full_name}...", end="", flush=True)
            try:
                commits = list(repo.get_commits(since=since, author=user))
                total_commits += len(commits)
            except:
                pass
            try:
                prs = list(repo.get_pulls(state="all"))
                total_prs += len([pr for pr in prs if pr.created_at > since and pr.user.login == user.login])
            except:
                pass
            try:
                lang_data = repo.get_languages()
                for lang, bytes_count in lang_data.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except:
                pass
            print(" done")
        except Exception as e:
            print(f" error: {str(e)[:50]}")

    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:6]
    lang_str = " . ".join([lang for lang, _ in top_langs])

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Use HTML comment markers for safe replacement
    new_stats = f"""<!-- STATS_START -->
**🔥 {total_commits} Commits (Last 30 Days)** | **⚔️ {total_prs} Pull Requests** | **🛸 {total_repos} Total Repositories**

**📊 Primary Stack:** {lang_str}
<!-- STATS_END -->"""

    readme = re.sub(r"<!-- STATS_START -->.*?<!-- STATS_END -->", new_stats, readme, flags=re.DOTALL)

    new_portfolio = f"""<!-- PORTFOLIO_START -->
### 💀 **Portfolio Highlights**

- **{public_repos} Public Repositories** - Extensive open-source contributions ⚔️
- **{total_repos} Total Repositories** - Including {private_repos} private client work and commercial projects 🔥
- **{total_commits} Commits (Last 30 Days)** - Active development across AI/ML, Web3, and quantitative systems ⚡
- **{total_prs} Pull Requests (Last 30 Days)** - Collaborative development and code review leadership 👽
<!-- PORTFOLIO_END -->"""

    readme = re.sub(r"<!-- PORTFOLIO_START -->.*?<!-- PORTFOLIO_END -->", new_portfolio, readme, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("README updated!")


if __name__ == "__main__":
    main()
