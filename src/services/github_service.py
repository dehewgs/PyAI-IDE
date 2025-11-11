"""
GitHub integration service for PyAI IDE
Handles repository operations and GitHub API interactions
"""

from typing import Any, Dict, List, Optional, Tuple

from utils.validators import validate_token, validate_github_url


class GitHubService:
    """
    Service for GitHub integration
    Manages repository operations and API interactions
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub service.
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.github = None
        self.user = None
        self.repositories: Dict[str, Any] = {}
    
    def set_token(self, token: str) -> Tuple[bool, str]:
        """
        Set GitHub API token and authenticate.
        
        Args:
            token: GitHub personal access token
            
        Returns:
            Tuple of (success, message)
        """
        is_valid, error = validate_token(token, 'github')
        
        if not is_valid:
            return False, error
        
        try:
            from github import Github
            
            self.token = token
            self.github = Github(token)
            self.user = self.github.get_user()
            
            # Test authentication
            _ = self.user.login
            
            return True, f"Authenticated as {self.user.login}"
        
        except ImportError:
            return False, "PyGithub library not installed"
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def get_token(self) -> Optional[str]:
        """Get current GitHub token"""
        return self.token
    
    def is_authenticated(self) -> bool:
        """Check if authenticated with GitHub"""
        return self.github is not None and self.user is not None
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get authenticated user information.
        
        Returns:
            Dictionary with user information
        """
        if not self.is_authenticated():
            return {'error': 'Not authenticated'}
        
        try:
            return {
                'login': self.user.login,
                'name': self.user.name,
                'email': self.user.email,
                'bio': self.user.bio,
                'public_repos': self.user.public_repos,
                'followers': self.user.followers,
                'following': self.user.following,
            }
        except Exception as e:
            return {'error': str(e)}
    
    def create_repository(self, name: str, description: str = "", 
                         private: bool = False) -> Tuple[bool, str]:
        """
        Create a new repository.
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether repository should be private
            
        Returns:
            Tuple of (success, message/url)
        """
        if not self.is_authenticated():
            return False, "Not authenticated with GitHub"
        
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=True,
            )
            
            self.repositories[name] = repo
            return True, repo.html_url
        
        except Exception as e:
            return False, f"Failed to create repository: {str(e)}"
    
    def get_repository(self, repo_name: str) -> Optional[Any]:
        """
        Get a repository by name.
        
        Args:
            repo_name: Repository name
            
        Returns:
            Repository object or None
        """
        if not self.is_authenticated():
            return None
        
        try:
            if repo_name in self.repositories:
                return self.repositories[repo_name]
            
            repo = self.user.get_repo(repo_name)
            self.repositories[repo_name] = repo
            return repo
        
        except Exception as e:
            print(f"Error getting repository: {e}")
            return None
    
    def list_repositories(self) -> List[Dict[str, Any]]:
        """
        List all repositories for authenticated user.
        
        Returns:
            List of repository information dictionaries
        """
        if not self.is_authenticated():
            return []
        
        try:
            repos = []
            for repo in self.user.get_repos():
                repos.append({
                    'name': repo.name,
                    'url': repo.html_url,
                    'description': repo.description,
                    'private': repo.private,
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                })
            return repos
        
        except Exception as e:
            print(f"Error listing repositories: {e}")
            return []
    
    def clone_repository(self, repo_url: str, local_path: str) -> Tuple[bool, str]:
        """
        Clone a repository locally.
        
        Args:
            repo_url: Repository URL
            local_path: Local path to clone to
            
        Returns:
            Tuple of (success, message)
        """
        is_valid, error = validate_github_url(repo_url)
        if not is_valid:
            return False, error
        
        try:
            from git import Repo
            
            Repo.clone_from(repo_url, local_path)
            return True, f"Repository cloned to {local_path}"
        
        except ImportError:
            return False, "GitPython library not installed"
        except Exception as e:
            return False, f"Failed to clone repository: {str(e)}"
    
    def push_changes(self, repo_path: str, message: str) -> Tuple[bool, str]:
        """
        Push changes to repository.
        
        Args:
            repo_path: Path to local repository
            message: Commit message
            
        Returns:
            Tuple of (success, message)
        """
        try:
            from git import Repo
            
            repo = Repo(repo_path)
            
            # Add all changes
            repo.git.add(A=True)
            
            # Commit
            repo.index.commit(message)
            
            # Push
            origin = repo.remote(name='origin')
            origin.push()
            
            return True, "Changes pushed successfully"
        
        except ImportError:
            return False, "GitPython library not installed"
        except Exception as e:
            return False, f"Failed to push changes: {str(e)}"
    
    def pull_changes(self, repo_path: str) -> Tuple[bool, str]:
        """
        Pull changes from repository.
        
        Args:
            repo_path: Path to local repository
            
        Returns:
            Tuple of (success, message)
        """
        try:
            from git import Repo
            
            repo = Repo(repo_path)
            origin = repo.remote(name='origin')
            origin.pull()
            
            return True, "Changes pulled successfully"
        
        except ImportError:
            return False, "GitPython library not installed"
        except Exception as e:
            return False, f"Failed to pull changes: {str(e)}"
    
    def create_issue(self, repo_name: str, title: str, 
                    body: str = "") -> Tuple[bool, str]:
        """
        Create an issue in a repository.
        
        Args:
            repo_name: Repository name
            title: Issue title
            body: Issue description
            
        Returns:
            Tuple of (success, message/url)
        """
        repo = self.get_repository(repo_name)
        if not repo:
            return False, "Repository not found"
        
        try:
            issue = repo.create_issue(title=title, body=body)
            return True, issue.html_url
        
        except Exception as e:
            return False, f"Failed to create issue: {str(e)}"
    
    def create_pull_request(self, repo_name: str, title: str, 
                           head: str, base: str = "main",
                           body: str = "") -> Tuple[bool, str]:
        """
        Create a pull request.
        
        Args:
            repo_name: Repository name
            title: PR title
            head: Head branch
            base: Base branch
            body: PR description
            
        Returns:
            Tuple of (success, message/url)
        """
        repo = self.get_repository(repo_name)
        if not repo:
            return False, "Repository not found"
        
        try:
            pr = repo.create_pull(title=title, head=head, base=base, body=body)
            return True, pr.html_url
        
        except Exception as e:
            return False, f"Failed to create pull request: {str(e)}"
