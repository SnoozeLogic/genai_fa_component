#!/usr/bin/env python3
"""
Test GitHub API access without authentication (public repos only)
"""
import os
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from edutrack.api.github_handler import GitHubHandler

def test_public_repo_access():
    """Test accessing public repositories without authentication"""
    print("=" * 70)
    print("🧪 Testing GitHub API - Public Repository Access")
    print("=" * 70)
    print()
    
    handler = GitHubHandler()
    
    if handler.authenticated:
        print("✅ Using authenticated access (with token)")
        print(f"   Rate limit: 5,000 requests/hour")
    else:
        print("⚠️  Using unauthenticated access (no token)")
        print(f"   Rate limit: 60 requests/hour per IP")
    print()
    
    # Test with a well-known public repository
    test_repos = [
        "https://github.com/django/django",
        "https://github.com/python/cpython",
    ]
    
    print(f"📦 Testing with public repository...")
    print(f"   Repo: {test_repos[0]}")
    print()
    
    try:
        print("🔍 Fetching repository data...")
        data = handler.fetch_repo_data(test_repos[0])
        
        if data.get('success'):
            print("✅ Successfully fetched data!")
            print()
            print("📊 Repository Information:")
            print(f"   Name: {data.get('repo_name')}")
            print(f"   Commits found: {data.get('commit_count')}")
            print(f"   Languages: {', '.join(data.get('languages', {}).keys())}")
            print(f"   Contributors: {len(data.get('contributors', []))}")
            print(f"   Has README: {'Yes' if data.get('readme_content') else 'No'}")
            print()
            
            if data.get('last_commit'):
                commit = data['last_commit']
                print("📝 Latest Commit:")
                print(f"   Message: {commit.get('message', 'N/A')[:60]}...")
                print(f"   Date: {commit.get('date', 'N/A')}")
                print(f"   Author: {commit.get('author', 'N/A')}")
            print()
            
            print("=" * 70)
            print("✅ PUBLIC REPO ACCESS WORKS!")
            print("=" * 70)
            print()
            print("💡 Key Points:")
            print()
            if handler.authenticated:
                print("   ✅ You have a token configured")
                print("   ✅ Can access private repos")
                print("   ✅ 5,000 requests/hour limit")
            else:
                print("   ⚠️  No token configured (this is OK for public repos!)")
                print("   ✅ Can access all public repos")
                print("   ⚠️  Only 60 requests/hour limit")
                print()
                print("   💡 If you hit rate limits, add a token:")
                print("      1. Visit: https://github.com/settings/tokens")
                print("      2. Generate new token (classic)")
                print("      3. Select 'repo' scope")
                print("      4. Add to .env: GITHUB_TOKEN=your_token_here")
            print()
            return True
            
        else:
            print(f"❌ Error: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        if "rate limit" in str(e).lower():
            print("💡 You've hit the rate limit!")
            print("   Add a GitHub token to increase from 60 to 5,000 requests/hour")
        return False

if __name__ == "__main__":
    success = test_public_repo_access()
    sys.exit(0 if success else 1)
