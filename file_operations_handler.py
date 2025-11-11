"""
File Operations Handler - Section 2 of Claude Code Plan
Handles all file system operations with safety checks and validation
"""

import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from tools_registry import FileReadTool, FileWriterTool, DirectoryReadTool


class FileOperationsHandler:
    """Handles file operations following Claude Code logic chains."""
    
    def __init__(self):
        """Initialize file operations handler."""
        self.file_read_tool = FileReadTool()
        try:
            self.file_write_tool = FileWriterTool()
            self.directory_read_tool = DirectoryReadTool()
        except Exception:
            self.file_write_tool = None
            self.directory_read_tool = None
    
    def create_file(self, file_path: str, content: str = "", context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a file following Section 2.1 logic chain.
        
        Args:
            file_path: Path to file to create
            content: Content to write
            context: Optional context
            
        Returns:
            Result dictionary
        """
        # PATH RESOLUTION
        resolved_path = self._resolve_path(file_path, context)
        
        # EXISTENCE CHECK
        if os.path.exists(resolved_path):
            return {
                "success": False,
                "error": "File already exists",
                "path": resolved_path,
                "action": "overwrite_required"
            }
        
        # DIRECTORY CHECK
        parent_dir = os.path.dirname(resolved_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        
        # CONTENT GENERATION & VALIDATION
        validated_content = self._validate_content(content, resolved_path)
        
        # WRITE OPERATION
        try:
            with open(resolved_path, 'w', encoding='utf-8') as f:
                f.write(validated_content)
            
            return {
                "success": True,
                "path": resolved_path,
                "action": "created",
                "size": len(validated_content)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": resolved_path
            }
    
    def read_file(self, file_path: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Read a file following Claude Code logic.
        
        Args:
            file_path: Path to file
            context: Optional context
            
        Returns:
            File content and metadata
        """
        resolved_path = self._resolve_path(file_path, context)
        
        if not os.path.exists(resolved_path):
            return {
                "success": False,
                "error": "File not found",
                "path": resolved_path
            }
        
        if not os.path.isfile(resolved_path):
            return {
                "success": False,
                "error": "Path is not a file",
                "path": resolved_path
            }
        
        try:
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "path": resolved_path,
                "content": content,
                "size": len(content),
                "lines": len(content.splitlines())
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": resolved_path
            }
    
    def modify_file(self, file_path: str, modifications: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Modify a file following Section 2.2 logic.
        
        Args:
            file_path: Path to file
            modifications: Dict with modification instructions
            context: Optional context
            
        Returns:
            Result dictionary
        """
        resolved_path = self._resolve_path(file_path, context)
        
        # Read existing content
        read_result = self.read_file(resolved_path, context)
        if not read_result["success"]:
            return read_result
        
        original_content = read_result["content"]
        
        # Apply modifications
        modified_content = self._apply_modifications(original_content, modifications)
        
        # VALIDATION LAYER
        validation = self._validate_modification(original_content, modified_content, resolved_path)
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"],
                "path": resolved_path
            }
        
        # Write modified content
        try:
            # Backup original
            backup_path = f"{resolved_path}.bak"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write modified
            with open(resolved_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            return {
                "success": True,
                "path": resolved_path,
                "backup": backup_path,
                "changes": validation["changes"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": resolved_path
            }
    
    def delete_file(self, file_path: str, context: Optional[Dict] = None, confirmed: bool = False) -> Dict[str, Any]:
        """
        Delete a file following Section 2.3 logic with risk assessment.
        
        Args:
            file_path: Path to file
            context: Optional context
            confirmed: Whether deletion is confirmed
            
        Returns:
            Result dictionary
        """
        resolved_path = self._resolve_path(file_path, context)
        
        # RISK ASSESSMENT
        risk = self._assess_deletion_risk(resolved_path)
        
        if risk["level"] == "critical" and not confirmed:
            return {
                "success": False,
                "error": "Deletion blocked - critical file",
                "risk": risk,
                "requires_confirmation": True
            }
        
        if not os.path.exists(resolved_path):
            return {
                "success": False,
                "error": "File does not exist",
                "path": resolved_path
            }
        
        try:
            os.remove(resolved_path)
            return {
                "success": True,
                "path": resolved_path,
                "action": "deleted"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": resolved_path
            }
    
    def _resolve_path(self, file_path: str, context: Optional[Dict]) -> str:
        """Resolve file path (absolute, relative, or inferred)."""
        if os.path.isabs(file_path):
            return file_path
        
        if context and "current_directory" in context:
            return os.path.join(context["current_directory"], file_path)
        
        return os.path.join(os.getcwd(), file_path)
    
    def _validate_content(self, content: str, file_path: str) -> str:
        """Validate and prepare content for writing."""
        # Add boilerplate if needed
        extension = os.path.splitext(file_path)[1]
        
        if extension == ".py" and not content.strip().startswith("#"):
            # Add basic Python docstring if empty
            if not content.strip():
                content = '"""\nModule docstring\n"""\n\n'
        
        return content
    
    def _apply_modifications(self, content: str, modifications: Dict[str, Any]) -> str:
        """Apply modifications to content."""
        modified = content
        
        if "replace" in modifications:
            old, new = modifications["replace"]
            modified = modified.replace(old, new)
        
        if "insert_at_line" in modifications:
            line_num, new_content = modifications["insert_at_line"]
            lines = modified.splitlines()
            lines.insert(line_num - 1, new_content)
            modified = "\n".join(lines)
        
        if "append" in modifications:
            modified += "\n" + modifications["append"]
        
        if "prepend" in modifications:
            modified = modifications["prepend"] + "\n" + modified
        
        return modified
    
    def _validate_modification(self, original: str, modified: str, file_path: str) -> Dict[str, Any]:
        """Validate file modification."""
        # Basic validation
        if len(modified) > 10_000_000:  # 10MB limit
            return {
                "valid": False,
                "error": "File too large after modification"
            }
        
        # Count changes
        changes = {
            "lines_added": len(modified.splitlines()) - len(original.splitlines()),
            "chars_changed": sum(1 for a, b in zip(original, modified) if a != b)
        }
        
        return {
            "valid": True,
            "changes": changes
        }
    
    def _assess_deletion_risk(self, file_path: str) -> Dict[str, Any]:
        """Assess risk of deleting a file."""
        risk_level = "low"
        reasons = []
        
        # Check if system file
        system_paths = ["/System", "/usr", "/bin", "/sbin", "/etc"]
        if any(file_path.startswith(sp) for sp in system_paths):
            risk_level = "critical"
            reasons.append("System file")
        
        # Check if git repository
        if ".git" in file_path:
            risk_level = "high"
            reasons.append("Git repository file")
        
        # Check if node_modules or dependencies
        if "node_modules" in file_path or "venv" in file_path:
            risk_level = "medium"
            reasons.append("Dependency directory")
        
        return {
            "level": risk_level,
            "reasons": reasons
        }


# Global instance
_file_handler = None

def get_file_handler() -> FileOperationsHandler:
    """Get or create global file operations handler."""
    global _file_handler
    if _file_handler is None:
        _file_handler = FileOperationsHandler()
    return _file_handler

