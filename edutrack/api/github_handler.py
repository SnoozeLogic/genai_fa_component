"""
GitHub API Handler for fetching repository data
"""
import requests
import base64
from datetime import datetime
from django.conf import settings


class GitHubHandler:
    """
    Handler for GitHub API operations
    
    Works with or without authentication:
    - WITHOUT TOKEN: 60 requests/hour per IP (public repos only)
    - WITH TOKEN: 5,000 requests/hour (public + private repos)
    """
    
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        
        # Set headers based on whether token is available
        if self.token and self.token != 'your_github_token_here':
            self.headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            self.authenticated = True
        else:
            self.headers = {
                "Accept": "application/vnd.github.v3+json"
            }
            self.authenticated = False
    
    def parse_repo_url(self, repo_url):
        """
        Extract owner and repo name from GitHub URL
        Example: https://github.com/owner/repo -> owner/repo
        """
        if "github.com/" in repo_url:
            parts = repo_url.split("github.com/")[-1].strip("/").split("/")
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
        return None
    
    def fetch_repo_data(self, repo_url):
        """
        Fetch comprehensive repository data from GitHub
        Returns a dictionary with all relevant information
        
        Works without authentication for public repos (60 requests/hour limit)
        """
        repo_name = self.parse_repo_url(repo_url)
        if not repo_name:
            return {"error": "Invalid GitHub URL"}
        
        try:
            # Fetch basic repo info
            repo_info = self._get_repo_info(repo_name)
            
            # Fetch commits
            commits = self._get_commits(repo_name)
            
            # Fetch languages
            languages = self._get_languages(repo_name)
            
            # Fetch README
            readme = self._get_readme(repo_name)
            
            # Fetch contributors
            contributors = self._get_contributors(repo_name)
            
            return {
                "success": True,
                "repo_name": repo_name,
                "commit_count": len(commits),
                "commits": commits[:10],  # Last 10 commits
                "last_commit": commits[0] if commits else None,
                "languages": languages,
                "readme_content": readme,
                "contributors": contributors,
                "repo_info": repo_info,
                "authenticated": self.authenticated,
                "fetched_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "repo_name": repo_name
            }
    
    def _get_repo_info(self, repo_name):
        """Get basic repository information"""
        url = f"{self.base_url}/repos/{repo_name}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "name": data.get("name"),
                "description": data.get("description"),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "default_branch": data.get("default_branch", "main")
            }
        return {}
    
    def _get_commits(self, repo_name):
        """Fetch repository commits"""
        url = f"{self.base_url}/repos/{repo_name}/commits"
        response = requests.get(url, headers=self.headers, params={"per_page": 100})
        
        if response.status_code == 200:
            commits_data = response.json()
            commits = []
            for commit in commits_data:
                commits.append({
                    "sha": commit.get("sha"),
                    "message": commit.get("commit", {}).get("message"),
                    "date": commit.get("commit", {}).get("author", {}).get("date"),
                    "author": commit.get("commit", {}).get("author", {}).get("name")
                })
            return commits
        return []
    
    def _get_languages(self, repo_name):
        """Fetch programming languages used in the repository"""
        url = f"{self.base_url}/repos/{repo_name}/languages"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return {}
    
    def _get_readme(self, repo_name):
        """Fetch README content"""
        url = f"{self.base_url}/repos/{repo_name}/readme"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("content", "")
            try:
                # README content is base64 encoded
                decoded_content = base64.b64decode(content).decode('utf-8')
                return decoded_content[:2000]  # First 2000 chars
            except Exception:
                return ""
        return ""
    
    def _get_contributors(self, repo_name):
        """Fetch repository contributors"""
        url = f"{self.base_url}/repos/{repo_name}/contributors"
        response = requests.get(url, headers=self.headers, params={"per_page": 10})
        
        if response.status_code == 200:
            contributors_data = response.json()
            contributors = []
            for contributor in contributors_data:
                contributors.append({
                    "login": contributor.get("login"),
                    "contributions": contributor.get("contributions")
                })
            return contributors
        return []
    
    def get_activity_stats(self, commits):
        """
        Calculate activity statistics from commits
        """
        if not commits:
            return {
                "total_commits": 0,
                "recent_activity": "No recent activity",
                "commit_frequency": "Unknown"
            }
        
        # Count commits in last 7 days
        from datetime import datetime, timedelta
        
        recent_commits = 0
        week_ago = datetime.now() - timedelta(days=7)
        
        for commit in commits:
            commit_date_str = commit.get("date")
            if commit_date_str:
                commit_date = datetime.fromisoformat(commit_date_str.replace('Z', '+00:00'))
                if commit_date.replace(tzinfo=None) > week_ago:
                    recent_commits += 1
        
        return {
            "total_commits": len(commits),
            "recent_commits_7days": recent_commits,
            "recent_activity": f"{recent_commits} commits in last 7 days",
            "commit_frequency": "Active" if recent_commits > 0 else "Inactive"
        }
