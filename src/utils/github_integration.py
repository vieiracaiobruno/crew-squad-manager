"""
GitHub Integration utilities using Composio
"""
import os
from typing import Dict, List, Optional
from loguru import logger
from composio import Composio, Action

class GitHubIntegration: 
    """
    Handle GitHub operations using Composio
    """
    
    def __init__(self):
        """Initialize GitHub integration with Composio"""
        self. composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
        self.repo_owner = os.getenv("GITHUB_REPO_OWNER")
        self.repo_name = os.getenv("GITHUB_REPO_NAME")
        
    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict:
        """
        Create a new GitHub issue
        
        Args: 
            title: Issue title
            body: Issue description
            labels: List of labels to add
            assignees: List of assignees
            
        Returns:
            Dict with issue information
        """
        try: 
            logger.info(f"Creating issue: {title}")
            
            result = self.composio.execute_action(
                action=Action.GITHUB_CREATE_ISSUE,
                params={
                    "owner": self.repo_owner,
                    "repo": self.repo_name,
                    "title": title,
                    "body": body,
                    "labels": labels or [],
                    "assignees":  assignees or []
                }
            )
            
            logger. success(f"Issue created: #{result. get('number')}")
            return result
            
        except Exception as e: 
            logger.error(f"Error creating issue: {str(e)}")
            raise
    
    def update_issue(
        self,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> Dict:
        """
        Update an existing GitHub issue
        
        Args:
            issue_number: Issue number
            title: New title
            body: New body
            state: New state (open/closed)
            labels:  New labels
            
        Returns: 
            Dict with updated issue information
        """
        try:
            logger.info(f"Updating issue #{issue_number}")
            
            params = {
                "owner": self.repo_owner,
                "repo": self.repo_name,
                "issue_number": issue_number
            }
            
            if title:
                params["title"] = title
            if body:
                params["body"] = body
            if state:
                params["state"] = state
            if labels: 
                params["labels"] = labels
            
            result = self.composio.execute_action(
                action=Action.GITHUB_UPDATE_ISSUE,
                params=params
            )
            
            logger.success(f"Issue #{issue_number} updated")
            return result
            
        except Exception as e:
            logger.error(f"Error updating issue:  {str(e)}")
            raise
    
    def add_comment(self, issue_number: int, comment: str) -> Dict:
        """
        Add a comment to an issue
        
        Args:
            issue_number: Issue number
            comment: Comment text
            
        Returns:
            Dict with comment information
        """
        try: 
            logger.info(f"Adding comment to issue #{issue_number}")
            
            result = self. composio.execute_action(
                action=Action.GITHUB_CREATE_ISSUE_COMMENT,
                params={
                    "owner": self.repo_owner,
                    "repo": self.repo_name,
                    "issue_number": issue_number,
                    "body": comment
                }
            )
            
            logger.success(f"Comment added to issue #{issue_number}")
            return result
            
        except Exception as e: 
            logger.error(f"Error adding comment: {str(e)}")
            raise
    
    def close_issue(self, issue_number: int) -> Dict:
        """
        Close an issue
        
        Args:
            issue_number: Issue number
            
        Returns:
            Dict with issue information
        """
        return self.update_issue(issue_number, state="closed")
    
    def get_repository_content(self, path: str = "") -> Dict:
        """
        Get repository content
        
        Args: 
            path: Path to content
            
        Returns:
            Dict with content information
        """
        try: 
            logger.info(f"Getting repository content:  {path}")
            
            result = self.composio.execute_action(
                action=Action. GITHUB_GET_CONTENT,
                params={
                    "owner": self.repo_owner,
                    "repo": self.repo_name,
                    "path": path
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting repository content: {str(e)}")
            raise