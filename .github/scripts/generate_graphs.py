#!/usr/bin/env python3
"""Generate custom SVG visualizations for GitHub profile"""

import os
from datetime import datetime, timedelta
from github import Github
from collections import defaultdict

def generate_stats_card(stats):
    """Generate a large, impressive SVG stats card"""
    svg = f'''<svg width="800" height="320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F85D7F;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#3FB950;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#F85D7F;stop-opacity:0.3" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background with gradient overlay -->
  <rect width="800" height="320" fill="#0D1117" rx="15"/>
  <rect width="800" height="320" fill="url(#grad2)" rx="15" opacity="0.1"/>
  
  <!-- Title Section -->
  <text x="400" y="50" font-family="'Segoe UI', Arial, sans-serif" font-size="28" font-weight="bold" fill="url(#grad1)" text-anchor="middle" filter="url(#glow)">
    ⚔️ REAL GITHUB IMPACT ⚔️
  </text>
  <text x="400" y="75" font-family="'Segoe UI', Arial, sans-serif" font-size="14" fill="#8B949E" text-anchor="middle">
    Public + Private Work • All 318 Repositories
  </text>
  
  <!-- Main Stats Grid -->
  <g transform="translate(80, 120)">
    <!-- Commits Box -->
    <rect x="-20" y="-30" width="200" height="110" fill="#161B22" rx="10" stroke="#F85D7F" stroke-width="2" opacity="0.8"/>
    <text x="90" y="0" font-family="'Segoe UI', Arial, sans-serif" font-size="48" fill="#F85D7F" font-weight="bold" text-anchor="middle">
      {stats['commits']}
    </text>
    <text x="90" y="25" font-family="'Segoe UI', Arial, sans-serif" font-size="14" fill="#C9D1D9" text-anchor="middle">
      🔥 COMMITS
    </text>
    <text x="90" y="45" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#8B949E" text-anchor="middle">
      Last 30 Days
    </text>
    
    <!-- Repos Box -->
    <rect x="220" y="-30" width="200" height="110" fill="#161B22" rx="10" stroke="#8B5CF6" stroke-width="2" opacity="0.8"/>
    <text x="310" y="0" font-family="'Segoe UI', Arial, sans-serif" font-size="48" fill="#8B5CF6" font-weight="bold" text-anchor="middle">
      {stats['total_repos']}
    </text>
    <text x="310" y="25" font-family="'Segoe UI', Arial, sans-serif" font-size="14" fill="#C9D1D9" text-anchor="middle">
      🛸 REPOSITORIES
    </text>
    <text x="310" y="45" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#8B949E" text-anchor="middle">
      {stats['public_repos']} Public • {stats['private_repos']} Private
    </text>
    
    <!-- PRs Box -->
    <rect x="460" y="-30" width="200" height="110" fill="#161B22" rx="10" stroke="#3FB950" stroke-width="2" opacity="0.8"/>
    <text x="550" y="0" font-family="'Segoe UI', Arial, sans-serif" font-size="48" fill="#3FB950" font-weight="bold" text-anchor="middle">
      {stats['prs']}
    </text>
    <text x="550" y="25" font-family="'Segoe UI', Arial, sans-serif" font-size="14" fill="#C9D1D9" text-anchor="middle">
      ⚔️ PULL REQUESTS
    </text>
    <text x="550" y="45" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#8B949E" text-anchor="middle">
      Last 30 Days
    </text>
  </g>
  
  <!-- Tech Stack Bar -->
  <rect x="80" y="250" width="640" height="40" fill="#161B22" rx="8" opacity="0.6"/>
  <text x="400" y="275" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="#C9D1D9" text-anchor="middle">
    💀 Primary Stack: {stats['top_languages']}
  </text>
  
  <!-- Last Updated -->
  <text x="400" y="310" font-family="'Segoe UI', Arial, sans-serif" font-size="10" fill="#6E7681" text-anchor="middle">
    🤖 Auto-Updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
  </text>
</svg>'''
    return svg


def generate_language_chart(languages):
    """Generate a large, impressive language distribution bar chart with infographic styling"""
    total_bytes = sum(languages.values())
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:8]
    
    colors = {
        'Python': '#3572A5',
        'TypeScript': '#3178C6', 
        'JavaScript': '#F1E05A',
        'Jupyter Notebook': '#DA5B0B',
        'C#': '#178600',
        'C': '#555555',
        'Go': '#00ADD8',
        'Rust': '#DEA584',
        'Solidity': '#AA6746',
        'HTML': '#E34C26',
        'CSS': '#563D7C',
        'Java': '#B07219',
        'Ruby': '#701516',
        'PHP': '#4F5D95',
        'Swift': '#F05138',
        'Kotlin': '#A97BFF'
    }
    
    svg = f'''<svg width="800" height="500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#F85D7F;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#8B5CF6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3FB950;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="800" height="500" fill="#0D1117" rx="15"/>
  
  <!-- Title Section -->
  <text x="400" y="45" font-family="'Segoe UI', Arial, sans-serif" font-size="28" font-weight="bold" fill="url(#titleGrad)" text-anchor="middle">
    💀 TECH STACK BREAKDOWN
  </text>
  <text x="400" y="70" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="#8B949E" text-anchor="middle">
    Language Distribution Across All Repositories
  </text>
  
  <!-- Language Bars -->
'''
    
    y_offset = 110
    bar_height = 40
    bar_spacing = 45
    max_bar_width = 600
    
    for i, (lang, bytes_count) in enumerate(top_langs):
        percentage = (bytes_count / total_bytes) * 100
        bar_width = (bytes_count / total_bytes) * max_bar_width
        color = colors.get(lang, '#858585')
        
        svg += f'''  <g transform="translate(80, {y_offset + i * bar_spacing})">
    <!-- Bar background -->
    <rect x="0" y="0" width="{max_bar_width}" height="{bar_height}" fill="#161B22" rx="8" opacity="0.5"/>
    <!-- Colored bar -->
    <rect x="0" y="0" width="{bar_width}" height="{bar_height}" fill="{color}" rx="8" filter="url(#shadow)" opacity="0.9"/>
    
    <!-- Language name -->
    <text x="15" y="{bar_height/2 + 5}" font-family="'Segoe UI', Arial, sans-serif" font-size="16" fill="#C9D1D9" font-weight="600">
      {lang}
    </text>
    
    <!-- Percentage -->
    <text x="{max_bar_width - 15}" y="{bar_height/2 + 5}" font-family="'Segoe UI', Arial, sans-serif" font-size="16" fill="#C9D1D9" text-anchor="end" font-weight="bold">
      {percentage:.1f}%
    </text>
  </g>
'''
    
    svg += f'''
  <!-- Footer -->
  <text x="400" y="480" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#6E7681" text-anchor="middle">
    🤖 Based on {len(languages)} languages • Updated: {datetime.now().strftime('%B %d, %Y')}
  </text>
</svg>'''
    return svg


def generate_activity_chart(commits_by_week):
    """Generate a large, impressive commit activity chart with infographic styling"""
    max_commits = max(commits_by_week) if commits_by_week else 1
    total_commits = sum(commits_by_week)
    
    svg = f'''<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3FB950;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0D1117;stop-opacity:0.8" />
    </linearGradient>
    <linearGradient id="titleGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#3FB950;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#F85D7F;stop-opacity:1" />
    </linearGradient>
    <filter id="glow2">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="800" height="400" fill="#0D1117" rx="15"/>
  
  <!-- Title Section -->
  <text x="400" y="45" font-family="'Segoe UI', Arial, sans-serif" font-size="28" font-weight="bold" fill="url(#titleGrad2)" text-anchor="middle">
    ⚡ 30-DAY COMMIT ACTIVITY
  </text>
  <text x="400" y="70" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="#8B949E" text-anchor="middle">
    Total: {total_commits} commits • Peak: {max_commits} commits/day
  </text>
  
  <!-- Chart Area -->
  <rect x="60" y="100" width="680" height="240" fill="#161B22" rx="10" opacity="0.3"/>
  
  <!-- Chart -->
  <g transform="translate(80, 120)">
'''
    
    bar_width = 640 / len(commits_by_week) if commits_by_week else 10
    chart_height = 180
    
    for i, commits in enumerate(commits_by_week):
        bar_height = (commits / max_commits) * chart_height if max_commits > 0 else 0
        x_pos = i * (bar_width + 2)
        y_pos = chart_height - bar_height
        
        # Color gradient based on activity level
        if commits == 0:
            color = '#21262D'
        elif commits >= max_commits * 0.7:
            color = '#3FB950'
        elif commits >= max_commits * 0.4:
            color = '#F85D7F'
        else:
            color = '#8B5CF6'
        
        svg += f'''
    <rect x="{x_pos}" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="3" filter="url(#glow2)" opacity="0.85"/>'''
    
    # Grid lines for reference
    for i in range(5):
        y = i * (chart_height / 4)
        svg += f'''
    <line x1="0" y1="{y}" x2="640" y2="{y}" stroke="#30363D" stroke-width="1" opacity="0.3"/>'''
    
    svg += f'''
  </g>
  
  <!-- Y-axis labels -->
  <text x="60" y="120" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#6E7681">{max_commits}</text>
  <text x="60" y="210" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#6E7681">{max_commits//2}</text>
  <text x="60" y="305" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#6E7681">0</text>
  
  <!-- Footer -->
  <text x="400" y="380" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#6E7681" text-anchor="middle">
    🤖 Real-time tracking • Updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
  </text>
</svg>'''
    return svg


def main():
    """Main function to generate all graphs"""
    print("🚀 Starting graph generation...")
    
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN not found!")
        return
    
    g = Github(token)
    user = g.get_user()
    
    # Initialize stats
    stats = {
        'commits': 0,
        'prs': 0,
        'total_repos': 0,
        'public_repos': 0,
        'private_repos': 0,
        'top_languages': ''
    }
    
    languages = defaultdict(int)
    commits_by_day = defaultdict(int)
    
    # Calculate date 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    print("📊 Scanning all repositories...")
    repos = list(user.get_repos(affiliation='owner'))
    stats['total_repos'] = len(repos)
    
    for repo in repos:
        if repo.private:
            stats['private_repos'] += 1
        else:
            stats['public_repos'] += 1
        
        # Count languages
        try:
            repo_langs = repo.get_languages()
            for lang, bytes_count in repo_langs.items():
                languages[lang] += bytes_count
        except Exception:
            pass
        
        # Count commits in last 30 days
        try:
            commits = repo.get_commits(since=thirty_days_ago, author=user)
            for commit in commits:
                stats['commits'] += 1
                commit_date = commit.commit.author.date.date()
                commits_by_day[commit_date] += 1
        except Exception:
            pass
        
        # Count PRs
        try:
            prs = repo.get_pulls(state='all', sort='created', direction='desc')
            for pr in prs:
                if pr.created_at >= thirty_days_ago and pr.user.login == user.login:
                    stats['prs'] += 1
        except Exception:
            pass
    
    # Get top 5 languages for stats card
    top_5_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
    stats['top_languages'] = ' · '.join([lang for lang, _ in top_5_langs])
    
    # Generate 30-day commit array
    commits_by_week = []
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).date()
        commits_by_week.append(commits_by_day.get(date, 0))
    
    print(f"📈 Stats: {stats['commits']} commits, {stats['prs']} PRs, {stats['total_repos']} repos")
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Generate and save graphs
    print("🎨 Generating stats card...")
    with open('assets/github-stats.svg', 'w') as f:
        f.write(generate_stats_card(stats))
    
    print("🎨 Generating language chart...")
    with open('assets/language-chart.svg', 'w') as f:
        f.write(generate_language_chart(languages))
    
    print("🎨 Generating activity chart...")
    with open('assets/activity-chart.svg', 'w') as f:
        f.write(generate_activity_chart(commits_by_week))
    
    print("✅ All graphs generated successfully!")


if __name__ == '__main__':
    main()
