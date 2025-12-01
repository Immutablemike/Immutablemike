#!/usr/bin/env python3
"""
Generate custom SVG graphs for GitHub stats using real private+public data
"""

import os
import sys
from datetime import datetime, timedelta
from github import Github


def generate_stats_card(stats):
    """Generate a custom SVG stats card"""
    svg = f'''<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F85D7F;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="500" height="200" fill="#0D1117" rx="10"/>
  
  <!-- Title -->
  <text x="250" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="url(#grad1)" text-anchor="middle">
    ⚔️ Real GitHub Stats (Public + Private)
  </text>
  
  <!-- Stats Grid -->
  <g transform="translate(50, 60)">
    <!-- Commits -->
    <text x="0" y="20" font-family="Arial, sans-serif" font-size="14" fill="#F85D7F" font-weight="bold">
      🔥 {stats['commits']}
    </text>
    <text x="0" y="40" font-family="Arial, sans-serif" font-size="11" fill="#8B949E">
      Commits (30d)
    </text>
    
    <!-- Repos -->
    <text x="150" y="20" font-family="Arial, sans-serif" font-size="14" fill="#8B5CF6" font-weight="bold">
      🛸 {stats['total_repos']}
    </text>
    <text x="150" y="40" font-family="Arial, sans-serif" font-size="11" fill="#8B949E">
      Total Repos
    </text>
    
    <!-- Pull Requests -->
    <text x="300" y="20" font-family="Arial, sans-serif" font-size="14" fill="#3FB950" font-weight="bold">
      ⚔️ {stats['prs']}
    </text>
    <text x="300" y="40" font-family="Arial, sans-serif" font-size="11" fill="#8B949E">
      Pull Requests
    </text>
  </g>
  
  <!-- Repo Breakdown -->
  <g transform="translate(50, 130)">
    <text x="0" y="0" font-family="Arial, sans-serif" font-size="12" fill="#C9D1D9">
      📊 {stats['public_repos']} Public · {stats['private_repos']} Private
    </text>
    <text x="0" y="20" font-family="Arial, sans-serif" font-size="10" fill="#8B949E">
      Top: {stats['top_languages']}
    </text>
  </g>
  
  <!-- Last Updated -->
  <text x="250" y="190" font-family="Arial, sans-serif" font-size="9" fill="#6E7681" text-anchor="middle">
    Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    return svg


def generate_language_chart(languages):
    """Generate a horizontal bar chart for top languages"""
    total_bytes = sum(languages.values())
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:6]
    
    colors = {
        'Python': '#3572A5',
        'TypeScript': '#3178C6', 
        'JavaScript': '#F1E05A',
        'Jupyter Notebook': '#DA5B0B',
        'C#': '#178600',
        'C': '#555555',
        'Go': '#00ADD8',
        'Rust': '#DEA584',
        'Solidity': '#AA6746'
    }
    
    svg = f'''<svg width="500" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="500" height="300" fill="#0D1117" rx="10"/>
  
  <!-- Title -->
  <text x="250" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#F85D7F" text-anchor="middle">
    💀 Language Distribution
  </text>
'''
    
    y_offset = 60
    for lang, bytes_count in top_langs:
        percentage = (bytes_count / total_bytes) * 100
        bar_width = (percentage / 100) * 350
        color = colors.get(lang, '#8B949E')
        
        svg += f'''
  <!-- {lang} -->
  <text x="30" y="{y_offset}" font-family="Arial, sans-serif" font-size="12" fill="#C9D1D9">
    {lang}
  </text>
  <rect x="130" y="{y_offset - 12}" width="{bar_width}" height="18" fill="{color}" rx="3"/>
  <text x="{140 + bar_width}" y="{y_offset}" font-family="Arial, sans-serif" font-size="11" fill="#8B949E">
    {percentage:.1f}%
  </text>
'''
        y_offset += 35
    
    svg += f'''
  <!-- Last Updated -->
  <text x="250" y="290" font-family="Arial, sans-serif" font-size="9" fill="#6E7681" text-anchor="middle">
    Generated from {len(languages)} languages across all repos
  </text>
</svg>'''
    return svg


def generate_activity_chart(commits_by_week):
    """Generate a commit activity chart"""
    max_commits = max(commits_by_week) if commits_by_week else 1
    
    svg = f'''<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="500" height="200" fill="#0D1117" rx="10"/>
  
  <!-- Title -->
  <text x="250" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#3FB950" text-anchor="middle">
    ⚡ 30-Day Commit Activity
  </text>
  
  <!-- Chart -->
  <g transform="translate(50, 60)">
'''
    
    bar_width = 380 / len(commits_by_week) if commits_by_week else 10
    for i, commits in enumerate(commits_by_week):
        bar_height = (commits / max_commits) * 100 if max_commits > 0 else 0
        x_pos = i * (bar_width + 2)
        y_pos = 100 - bar_height
        
        color = '#3FB950' if commits > 0 else '#21262D'
        
        svg += f'''
    <rect x="{x_pos}" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="2"/>
'''
    
    svg += f'''
  </g>
  
  <!-- Stats -->
  <text x="250" y="180" font-family="Arial, sans-serif" font-size="11" fill="#8B949E" text-anchor="middle">
    Total: {sum(commits_by_week)} commits | Peak: {max_commits} commits/day
  </text>
</svg>'''
    return svg


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not found!")
        sys.exit(1)

    g = Github(token)
    user = g.get_user()

    print(f"🔍 Generating graphs for {user.login}...")

    # Get all repos
    repos = list(user.get_repos(visibility="all"))
    total_repos = len(repos)
    public_repos = len([r for r in repos if not r.private])
    private_repos = len([r for r in repos if r.private])

    since = datetime.now() - timedelta(days=30)

    # Collect stats
    total_commits = 0
    total_prs = 0
    languages = {}
    commits_by_day = {}

    for i, repo in enumerate(repos, 1):
        try:
            print(f"  [{i}/{total_repos}] {repo.full_name}...", end="", flush=True)

            # Commits
            try:
                commits = list(repo.get_commits(since=since, author=user))
                total_commits += len(commits)
                for commit in commits:
                    day = commit.commit.author.date.strftime('%Y-%m-%d')
                    commits_by_day[day] = commits_by_day.get(day, 0) + 1
            except:
                pass

            # PRs
            try:
                prs = list(repo.get_pulls(state="all"))
                total_prs += len([pr for pr in prs if pr.created_at > since and pr.user.login == user.login])
            except:
                pass

            # Languages
            try:
                lang_data = repo.get_languages()
                for lang, bytes_count in lang_data.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except:
                pass

            print(" ✓")
        except Exception as e:
            print(f" ⚠️ {str(e)[:30]}")
            continue

    # Generate weekly commits for activity chart
    commits_by_week = []
    for i in range(30):
        day = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        commits_by_week.append(commits_by_day.get(day, 0))

    # Top languages string
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:6]
    lang_str = " · ".join([lang for lang, _ in top_langs])

    # Stats dict
    stats = {
        'commits': total_commits,
        'prs': total_prs,
        'total_repos': total_repos,
        'public_repos': public_repos,
        'private_repos': private_repos,
        'top_languages': lang_str[:50] + '...' if len(lang_str) > 50 else lang_str
    }

    print("\n🎨 Generating SVG graphs...")

    # Create assets directory
    os.makedirs('assets', exist_ok=True)

    # Generate SVGs
    with open('assets/github-stats.svg', 'w') as f:
        f.write(generate_stats_card(stats))
    print("  ✅ github-stats.svg")

    with open('assets/language-chart.svg', 'w') as f:
        f.write(generate_language_chart(languages))
    print("  ✅ language-chart.svg")

    with open('assets/activity-chart.svg', 'w') as f:
        f.write(generate_activity_chart(commits_by_week))
    print("  ✅ activity-chart.svg")

    print("\n✅ All graphs generated successfully!")


if __name__ == "__main__":
    main()
