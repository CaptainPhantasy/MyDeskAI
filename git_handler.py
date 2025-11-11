"""
Git Handler - Section 5 of Claude Code Plan
Handles all Git operations with safety checks
"""

import os
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path


class GitHandler:
    """Handles Git operations following Claude Code logic."""
    
    def __init__(self):
        """Initialize Git handler."""
        pass
    
    def check_repository_state(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Check repository state following Section 5.1 logic.
        
        Args:
            path: Repository path (defaults to current directory)
            
        Returns:
            Repository state information
        """
        repo_path = path or os.getcwd()
        
        # Is Git initialized?
        git_dir = os.path.join(repo_path, ".git")
        is_initialized = os.path.exists(git_dir)
        
        if not is_initialized:
            return {
                "initialized": False,
                "path": repo_path,
                "suggestion": "Run 'git init' to initialize"
            }
        
        # Working tree status
        status = self._get_status(repo_path)
        
        # Branch information
        branch_info = self._get_branch_info(repo_path)
        
        return {
            "initialized": True,
            "path": repo_path,
            "status": status,
            "branch": branch_info,
            "clean": status.get("clean", False)
        }
    
    def create_commit(self, message: Optional[str] = None, files: Optional[List[str]] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a commit following Section 5.1 commit strategy.
        
        Args:
            message: Commit message
            files: Files to commit (None = all)
            context: Optional context
            
        Returns:
            Commit result
        """
        repo_path = context.get("path") if context else os.getcwd()
        
        # Check repository state
        state = self.check_repository_state(repo_path)
        if not state["initialized"]:
            return {
                "success": False,
                "error": "Not a git repository"
            }
        
        # Change analysis
        changes = self._analyze_changes(repo_path, files)
        
        # Generate commit message if not provided
        if not message:
            message = self._generate_commit_message(changes)
        
        # Stage changes
        if files:
            for file in files:
                self._run_git_command(repo_path, ["add", file])
        else:
            self._run_git_command(repo_path, ["add", "."])
        
        # Create commit
        result = self._run_git_command(repo_path, ["commit", "-m", message])
        
        return {
            "success": result["success"],
            "message": message,
            "changes": changes,
            "commit_hash": result.get("output", "").strip() if result["success"] else None
        }
    
    def resolve_merge_conflict(self, conflict_path: str, strategy: str = "manual", context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Resolve merge conflicts following Section 5.2 logic.
        
        Args:
            conflict_path: Path to conflicted file
            strategy: Resolution strategy (theirs, ours, manual)
            context: Optional context
            
        Returns:
            Resolution result
        """
        repo_path = context.get("path") if context else os.getcwd()
        
        # Conflict analysis
        conflict_info = self._analyze_conflict(conflict_path)
        
        if strategy == "theirs":
            self._run_git_command(repo_path, ["checkout", "--theirs", conflict_path])
        elif strategy == "ours":
            self._run_git_command(repo_path, ["checkout", "--ours", conflict_path])
        elif strategy == "manual":
            # Return conflict markers for manual resolution
            return {
                "success": False,
                "requires_manual_resolution": True,
                "conflict_info": conflict_info,
                "file": conflict_path
            }
        
        # Stage resolved file
        self._run_git_command(repo_path, ["add", conflict_path])
        
        return {
            "success": True,
            "strategy": strategy,
            "file": conflict_path,
            "conflict_info": conflict_info
        }
    
    def _get_status(self, repo_path: str) -> Dict[str, Any]:
        """Get git status."""
        result = self._run_git_command(repo_path, ["status", "--porcelain"])
        
        if not result["success"]:
            return {"clean": False, "error": result.get("error")}
        
        output = result.get("output", "")
        has_changes = bool(output.strip())
        
        return {
            "clean": not has_changes,
            "changes": output.splitlines() if has_changes else []
        }
    
    def _get_branch_info(self, repo_path: str) -> Dict[str, Any]:
        """Get branch information."""
        branch_result = self._run_git_command(repo_path, ["branch", "--show-current"])
        remote_result = self._run_git_command(repo_path, ["branch", "-vv"])
        
        return {
            "current": branch_result.get("output", "").strip() if branch_result["success"] else "unknown",
            "remote_info": remote_result.get("output", "").strip() if remote_result["success"] else ""
        }
    
    def _analyze_changes(self, repo_path: str, files: Optional[List[str]]) -> Dict[str, Any]:
        """Analyze changes for commit."""
        if files:
            # Analyze specific files
            changes = []
            for file in files:
                diff_result = self._run_git_command(repo_path, ["diff", file])
                if diff_result["success"]:
                    changes.append({
                        "file": file,
                        "diff": diff_result.get("output", "")
                    })
        else:
            # Analyze all changes
            diff_result = self._run_git_command(repo_path, ["diff", "--cached"])
            changes = [{"all": diff_result.get("output", "")}]
        
        return {
            "files_changed": len(changes),
            "changes": changes
        }
    
    def _generate_commit_message(self, changes: Dict[str, Any]) -> str:
        """Generate commit message following conventional commits."""
        file_count = changes.get("files_changed", 0)
        
        # Simple conventional commit message
        return f"feat: update {file_count} file(s)"
    
    def _analyze_conflict(self, conflict_path: str) -> Dict[str, Any]:
        """Analyze merge conflict."""
        try:
            with open(conflict_path, 'r') as f:
                content = f.read()
            
            conflict_markers = content.count("<<<<<<<")
            
            return {
                "has_conflict": conflict_markers > 0,
                "conflict_count": conflict_markers,
                "file": conflict_path
            }
        except Exception as e:
            return {
                "has_conflict": False,
                "error": str(e)
            }
    
    def _run_git_command(self, repo_path: str, command: List[str]) -> Dict[str, Any]:
        """Run a git command safely."""
        try:
            full_command = ["git"] + command
            result = subprocess.run(
                full_command,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
_git_handler = None

def get_git_handler() -> GitHandler:
    """Get or create global Git handler."""
    global _git_handler
    if _git_handler is None:
        _git_handler = GitHandler()
    return _git_handler

