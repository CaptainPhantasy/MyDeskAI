"""
Terminal Handler - Section 8 of Claude Code Plan
Handles terminal command execution with safety checks
"""

import os
import subprocess
import shlex
from typing import Dict, List, Any, Optional
import platform


class TerminalHandler:
    """Handles terminal operations following Claude Code logic."""
    
    # Destructive commands that require confirmation
    DESTRUCTIVE_COMMANDS = [
        "rm", "del", "delete", "remove", "format", "fdisk",
        "dd", "mkfs", "shred", "wipe"
    ]
    
    # Dangerous patterns
    DANGEROUS_PATTERNS = [
        "rm -rf", "rm -r -f", "sudo rm", "format c:",
        "del /f /s", "rm -rf /", "rm -rf *"
    ]
    
    def __init__(self):
        """Initialize terminal handler."""
        self.platform = platform.system().lower()
    
    def execute_command(self, command: str, context: Optional[Dict] = None, confirmed: bool = False) -> Dict[str, Any]:
        """
        Execute a terminal command following Section 8.1 logic.
        
        Args:
            command: Command to execute
            context: Optional context
            confirmed: Whether command is confirmed (for destructive commands)
            
        Returns:
            Execution result
        """
        # COMMAND SAFETY CHECK
        safety_check = self._check_command_safety(command)
        
        if safety_check["requires_confirmation"] and not confirmed:
            return {
                "success": False,
                "error": "Destructive command requires confirmation",
                "safety_check": safety_check,
                "requires_confirmation": True
            }
        
        if safety_check["blocked"]:
            return {
                "success": False,
                "error": "Command blocked for safety",
                "safety_check": safety_check
            }
        
        # COMMAND CONSTRUCTION
        constructed_command = self._construct_command(command, context)
        
        # EXECUTION STRATEGY
        result = self._execute(constructed_command, context)
        
        # OUTPUT HANDLING
        processed_output = self._process_output(result)
        
        return processed_output
    
    def _check_command_safety(self, command: str) -> Dict[str, Any]:
        """Check command safety following Section 8.1 logic."""
        command_lower = command.lower()
        
        # Check for dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern in command_lower:
                return {
                    "safe": False,
                    "blocked": True,
                    "reason": f"Dangerous pattern: {pattern}",
                    "requires_confirmation": False
                }
        
        # Check for destructive commands
        for destructive in self.DESTRUCTIVE_COMMANDS:
            if command_lower.startswith(destructive) or f" {destructive} " in command_lower:
                return {
                    "safe": False,
                    "blocked": False,
                    "reason": f"Destructive command: {destructive}",
                    "requires_confirmation": True
                }
        
        # Check for system modification
        system_modifiers = ["sudo", "chmod", "chown", "install", "uninstall"]
        if any(mod in command_lower for mod in system_modifiers):
            return {
                "safe": False,
                "blocked": False,
                "reason": "System modification command",
                "requires_confirmation": True
            }
        
        return {
            "safe": True,
            "blocked": False,
            "requires_confirmation": False
        }
    
    def _construct_command(self, command: str, context: Optional[Dict]) -> List[str]:
        """Construct command with proper path handling."""
        # Handle platform differences
        if self.platform == "windows":
            # Windows command handling
            return ["cmd", "/c"] + shlex.split(command)
        else:
            # Unix-like command handling
            return shlex.split(command)
    
    def _execute(self, command: List[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Execute command safely."""
        cwd = context.get("current_directory") if context else os.getcwd()
        
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                shell=False
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(command)
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out",
                "command": " ".join(command)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": " ".join(command)
            }
    
    def _process_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process command output following Section 8.1 output handling."""
        output = result.get("stdout", "")
        error = result.get("stderr", "")
        
        # Handle large output
        if len(output) > 30000:
            output = output[:30000] + "\n... (truncated)"
        
        # Parse error messages
        error_summary = None
        if error:
            error_summary = self._parse_error(error)
        
        return {
            "success": result.get("success", False),
            "output": output,
            "error": error,
            "error_summary": error_summary,
            "returncode": result.get("returncode", -1),
            "command": result.get("command", "")
        }
    
    def _parse_error(self, error: str) -> Dict[str, Any]:
        """Parse error message for suggestions."""
        error_lower = error.lower()
        
        suggestions = []
        
        if "command not found" in error_lower:
            suggestions.append("Check if command is installed and in PATH")
        elif "permission denied" in error_lower:
            suggestions.append("Check file permissions or use sudo if appropriate")
        elif "no such file" in error_lower:
            suggestions.append("Verify file path exists")
        
        return {
            "message": error,
            "suggestions": suggestions
        }


# Global instance
_terminal_handler = None

def get_terminal_handler() -> TerminalHandler:
    """Get or create global terminal handler."""
    global _terminal_handler
    if _terminal_handler is None:
        _terminal_handler = TerminalHandler()
    return _terminal_handler

