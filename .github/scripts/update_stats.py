#!/usr/bin/env python3
"""
Enhanced GitHub stats generator with accurate PR counting.
Uses GitHub Search API to capture ALL contributions including:
- PRs authored (to own repos AND other repos)
- PRs merged 
- Contributions across the entire GitHub ecosystem
"""

import os
import re
import sys
from datetime import datetime, timedelta
from github import Github


def get_accurate_pr_count(g, username, since):
    """Use GitHub Search API to get accurate PR counts across ALL repos."""
    since_str = since.strftime("%Y-%m-%d")
    
    prs_authored = 0
    prs_merged = 0
    
    try:
        # PRs authored by user (anywhere on GitHub) in last 30 days
        query = f"author:{username} is:pr created:>={since_str}"
        results = g.search_issues(query)
        prs_authored = results.totalCount
        print(f"  📊 PRs authored (Search API): {prs_authored}")
    except Exception as e:
        print(f"  ⚠️  Could not search authored PRs: {e}")
    
    try:
        # PRs merged by user in last 30 days
        query = f"author:{username} is:pr is:merged merged:>={since_str}"
        results = g.search_issues(query)
        prs_merged = results.totalCount
        print(f"  📊 PRs merged (Search API): {prs_merged}")
    except Exception as e:
        print(f"  ⚠️  Could not search merged PRs: {e}")
    
    return prs_authored, prs_merged


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not found!")
        sys.exit(1)

    g = Github(token)
    user = g.get_user()
    username = user.login
    print(f"🚀 Fetching stats for {username}...")

    # Get repository counts
    repos = list(user.get_repos(visibility="all"))
    total_repos = len(repos)
    public_repos = len([r for r in repos if not r.private])
    private_repos = len([r for r in repos if r.private])
    print(f"📁 Found {total_repos} repos ({public_repos} public, {private_repos} private)")

    since = datetime.now() - timedelta(days=30)
    total_commits = 0
    languages = {}

    # Count commits and languages from user's repos
    print(f"\n📊 Analyzing {total_repos} repositories...")
    for i, repo in enumerate(repos, 1):
        try:
            if i % 50 == 0:
                print(f"  Progress: {i}/{total_repos} repos...")
            
            # Count commits
            try:
                commits = list(repo.get_commits(since=since, author=user))
                total_commits += len(commits)
            except Exception:
                pass
            
            # Count languages
            try:
                lang_data = repo.get_languages()
                for lang, bytes_count in lang_data.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except Exception:
                pass
        except Exception:
            pass

    # Get accurate PR count using Search API
    print("\n🔍 Getting accurate PR counts via Search API...")
    prs_authored, prs_merged = get_accurate_pr_count(g, username, since)
    total_prs = prs_authored  # Use authored count as primary metric

    # Calculate top languages
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:6]
    lang_str = " · ".join([lang for lang, _ in top_langs])

    print(f"\n📈 Final Stats Summary:")
    print(f"   Commits (30 days): {total_commits}")
    print(f"   PRs Authored (30 days): {prs_authored}")
    print(f"   PRs Merged (30 days): {prs_merged}")
    print(f"   Total Repos: {total_repos}")
    print(f"   Top Languages: {lang_str}")

    # Read README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Update stats section with HTML comment markers
    new_stats = f"""<!-- STATS_START -->
### 💀 **Real Stats** *(Public + Private)*

**🔥 {total_commits:,} Commits** *(Last 30 Days)* | **⚔️ {total_prs} Pull Requests** | **🛸 {total_repos:,} Repositories**

**📊 Primary Stack:** {lang_str}
<!-- STATS_END -->"""

    readme = re.sub(
        r"<!-- STATS_START -->.*?<!-- STATS_END -->",
        new_stats,
        readme,
        flags=re.DOTALL
    )

    # Update portfolio section
    new_portfolio = f"""<!-- PORTFOLIO_START -->
### 💀 **Portfolio Highlights**

| Metric | Count | Description |
|--------|-------|-------------|
| 🌐 **Public Repos** | {public_repos:,} | Open-source contributions ⚔️ |
| 🔒 **Total Repos** | {total_repos:,} | Including {private_repos} private projects 🔥 |
| 📈 **Commits** | {total_commits:,} | Active dev across AI/ML, Web3, quant ⚡ |
| 🔀 **Pull Requests** | {total_prs} | Code collaboration & review 👽 |
<!-- PORTFOLIO_END -->"""

    readme = re.sub(
        r"<!-- PORTFOLIO_START -->.*?<!-- PORTFOLIO_END -->",
        new_portfolio,
        readme,
        flags=re.DOTALL
    )

    # Update timestamp if present
    now = datetime.now().strftime("%B %Y")
    readme = re.sub(
        r"Profile Last Updated: \w+ \d{4}",
        f"Profile Last Updated: {now}",
        readme
    )

    # Write README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"\n✅ README.md updated successfully!")
    print(f"   File size: {len(readme):,} bytes")


if __name__ == "__main__":
    main()
