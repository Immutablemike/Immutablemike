#!/usr/bin/env python3
"""
Generate real GitHub stats from all repos (public + private) using PAT
"""

import os
import re
import sys
from datetime import datetime, timedelta

from github import Github


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not found!")
        sys.exit(1)

    g = Github(token)
    user = g.get_user()

    print(f"🔍 Fetching stats for {user.login}...")

    # Get all repos
    repos = list(user.get_repos(visibility="all"))
    total_repos = len(repos)
    public_repos = len([r for r in repos if not r.private])
    private_repos = len([r for r in repos if r.private])

    print(
        f"📊 Found {total_repos} total repos ({public_repos} public, {private_repos} private)"
    )

    # Calculate date range (last 30 days)
    since = datetime.now() - timedelta(days=30)

    # Count commits, PRs, issues
    total_commits = 0
    total_prs = 0
    total_issues = 0
    languages = {}

    for i, repo in enumerate(repos, 1):
        try:
            print(f"  [{i}/{total_repos}] {repo.full_name}...", end="", flush=True)

            # Count commits
            try:
                commits = list(repo.get_commits(since=since, author=user))
                total_commits += len(commits)
            except:
                pass

            # Count PRs
            try:
                prs = list(repo.get_pulls(state="all"))
                total_prs += len(
                    [
                        pr
                        for pr in prs
                        if pr.created_at > since and pr.user.login == user.login
                    ]
                )
            except:
                pass

            # Count Issues
            try:
                issues = list(repo.get_issues(state="all", creator=user.login))
                total_issues += len(
                    [
                        issue
                        for issue in issues
                        if not issue.pull_request and issue.created_at > since
                    ]
                )
            except:
                pass

            # Get languages
            try:
                lang_data = repo.get_languages()
                for lang, bytes_count in lang_data.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except:
                pass

            print(" ✓")

        except Exception as e:
            print(f" ⚠️ {str(e)[:50]}")
            continue

    # Top 6 languages
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:6]
    lang_str = " · ".join([lang for lang, _ in top_langs])

    print("\n📈 Results:")
    print(f"  Commits (30d): {total_commits}")
    print(f"  Pull Requests (30d): {total_prs}")
    print(f"  Issues (30d): {total_issues}")
    print(f"  Top Languages: {lang_str}")

    # Read README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Update stats section - match ANY text between the markers
    stats_pattern = r"(### 💀 \*\*Real Stats \(Public \+ Private Work\)\*\*\n\n)\*\*.*?\*\*( \| \*\*.*?\*\* \| \*\*.*?\*\*\n\n\*\*📊 Primary Stack:\*\*) .*"
    new_stats = f"\\1**🔥 {total_commits} Commits (Last 30 Days)** | **⚔️ {total_prs} Pull Requests** | **🛸 {total_repos} Total Repositories**\n\n**📊 Primary Stack:**\\2 {lang_str}"

    updated_readme = re.sub(stats_pattern, new_stats, readme)
    
    # If regex didn't match, try simpler approach
    if "### 💀 **Real Stats" in updated_readme and str(total_commits) not in updated_readme:
        # Simple line-by-line replacement
        lines = readme.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('**🔥'):
                lines[i] = f"**🔥 {total_commits} Commits (Last 30 Days)** | **⚔️ {total_prs} Pull Requests** | **🛸 {total_repos} Total Repositories**"
            elif line.startswith('**📊 Primary Stack:**'):
                lines[i] = f"**📊 Primary Stack:** {lang_str}"
        readme = '\n'.join(lines)
    else:
        readme = updated_readme

    # Update portfolio highlights - match ANY numbers
    highlights_pattern = r"(### 💀 \*\*Portfolio Highlights\*\*\n)- \*\*\d+.*?\*\*.*\n- \*\*\d+.*?\*\*.*\n- \*\*\d+.*?\*\*.*\n- \*\*\d+.*?\*\*.*\n"
    new_highlights = f"""\\1- **{public_repos} Public Repositories** - Extensive open-source contributions ⚔️
- **{total_repos} Total Repositories** - Including {private_repos} private client work and commercial projects 🔥
- **{total_commits} Commits (Last 30 Days)** - Active development across AI/ML, Web3, and quantitative systems ⚡
- **{total_prs} Pull Requests (Last 30 Days)** - Collaborative development and code review leadership 👽
"""

    readme = re.sub(highlights_pattern, new_highlights, readme)

    # Write updated README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("\n✅ README updated successfully!")


if __name__ == "__main__":
    main()
