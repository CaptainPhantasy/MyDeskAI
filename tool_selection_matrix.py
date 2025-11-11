"""
Tool Selection Matrix - Maps tasks to appropriate tools
Implements Appendix C of Claude Code Comprehensive Logic Plan
"""

from typing import Dict, List, Any, Optional
from tools_registry import get_tool_set, get_tools_by_category
from langchain_community.tools import ShellTool


class ToolSelectionMatrix:
    """
    Maps task types to appropriate tools based on Claude Code logic.
    Implements the tool selection matrix from the comprehensive logic plan.
    """
    
    # Task type to tool mapping (from Appendix C)
    TASK_TOOL_MAP = {
        # File Operations
        "create_single_file": {
            "primary": "write",
            "secondary": ["bash"],
            "conditions": "Parent dir must exist",
            "tool_set": "file_operations"
        },
        "create_multiple_files": {
            "primary": "write",
            "secondary": ["bash"],
            "conditions": "Related files",
            "tool_set": "file_operations"
        },
        "edit_single_file": {
            "primary": "edit",
            "secondary": ["write"],
            "conditions": "<5 changes",
            "tool_set": "file_operations"
        },
        "edit_multiple_spots": {
            "primary": "edit",
            "secondary": ["write"],
            "conditions": "Same file",
            "tool_set": "file_operations"
        },
        "read_file": {
            "primary": "read",
            "secondary": [],
            "conditions": "Always use Read tool",
            "tool_set": "file_operations"
        },
        "delete_files": {
            "primary": "bash",
            "secondary": [],
            "conditions": "With confirmation",
            "tool_set": "shell_operations"
        },
        
        # Search Operations
        "search_by_name": {
            "primary": "glob",
            "secondary": ["bash"],
            "conditions": "Pattern matching",
            "tool_set": "file_operations"
        },
        "search_by_content": {
            "primary": "grep",
            "secondary": ["bash"],
            "conditions": "Text in files",
            "tool_set": "file_operations"
        },
        "complex_search": {
            "primary": "task",
            "secondary": ["glob", "grep"],
            "conditions": "Multi-step exploration",
            "tool_set": "comprehensive"
        },
        
        # Code Operations
        "generate_code": {
            "primary": "write",
            "secondary": ["code_interpreter"],
            "conditions": "Code generation",
            "tool_set": "code_analysis"
        },
        "analyze_code": {
            "primary": "read",
            "secondary": ["code_interpreter", "github_search"],
            "conditions": "Code analysis",
            "tool_set": "code_analysis"
        },
        
        # Terminal Operations
        "run_commands": {
            "primary": "bash",
            "secondary": [],
            "conditions": "Check sandbox",
            "tool_set": "shell_operations"
        },
        "install_packages": {
            "primary": "bash",
            "secondary": [],
            "conditions": "Detect package manager",
            "tool_set": "shell_operations"
        },
        "test_execution": {
            "primary": "bash",
            "secondary": [],
            "conditions": "Platform-appropriate",
            "tool_set": "shell_operations"
        },
        
        # Web Operations
        "web_research": {
            "primary": "web_search",
            "secondary": ["web_fetch"],
            "conditions": "Current information",
            "tool_set": "web_research"
        },
        "documentation_lookup": {
            "primary": "web_fetch",
            "secondary": ["web_search"],
            "conditions": "Library docs",
            "tool_set": "web_research"
        },
        
        # Git Operations
        "git_operations": {
            "primary": "bash",
            "secondary": [],
            "conditions": "Follow git practices",
            "tool_set": "shell_operations"
        },
    }
    
    # Tool name to actual tool mapping
    TOOL_NAME_MAP = {
        "write": "FileWriterTool",
        "read": "FileReadTool",
        "edit": "FileReadTool",  # Edit uses read + write
        "bash": "ShellTool",
        "glob": "DirectorySearchTool",
        "grep": "ShellTool",  # grep via shell
        "code_interpreter": "CodeInterpreterTool",
        "github_search": "GithubSearchTool",
        "web_search": "SerperDevTool",
        "web_fetch": "WebsiteSearchTool",
        "task": "comprehensive",  # Use comprehensive tool set
    }
    
    def __init__(self):
        """Initialize the tool selection matrix."""
        pass
    
    def select_tools_for_task(self, task_type: str, context: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Select appropriate tools for a given task type.
        
        Args:
            task_type: Type of task (e.g., "create_single_file", "read_file")
            context: Optional context for tool selection
            
        Returns:
            List of tool instances
        """
        if task_type not in self.TASK_TOOL_MAP:
            # Default to comprehensive tool set
            return get_tool_set("comprehensive")
        
        task_config = self.TASK_TOOL_MAP[task_type]
        tool_set_name = task_config.get("tool_set", "comprehensive")
        
        # Get tools from the specified tool set
        tools = get_tool_set(tool_set_name)
        
        # Add shell tool if needed for bash operations
        if task_config["primary"] == "bash" or "bash" in task_config.get("secondary", []):
            try:
                shell_tool = ShellTool()
                if shell_tool not in tools:
                    tools.append(shell_tool)
            except Exception:
                pass  # ShellTool not available
        
        return tools
    
    def get_task_type_from_operation(self, operation_type: str, intent: str) -> Optional[str]:
        """
        Map operation type and intent to a specific task type.
        
        Args:
            operation_type: Type of operation (file_operation, code_operation, etc.)
            intent: User intent (create, read, write, etc.)
            
        Returns:
            Task type string or None
        """
        intent_lower = intent.lower()
        
        if operation_type == "file_operation":
            if "read" in intent_lower or "show" in intent_lower or "view" in intent_lower:
                return "read_file"
            elif "write" in intent_lower or "create" in intent_lower or "make" in intent_lower:
                return "create_single_file"
            elif "edit" in intent_lower or "modify" in intent_lower or "update" in intent_lower:
                return "edit_single_file"
            elif "delete" in intent_lower or "remove" in intent_lower:
                return "delete_files"
            elif "search" in intent_lower or "find" in intent_lower:
                return "search_by_name"
        
        elif operation_type == "code_operation":
            if "create" in intent_lower or "generate" in intent_lower:
                return "generate_code"
            elif "analyze" in intent_lower or "review" in intent_lower:
                return "analyze_code"
        
        elif operation_type == "git_operation":
            return "git_operations"
        
        elif operation_type == "search":
            if "grep" in intent_lower or "content" in intent_lower:
                return "search_by_content"
            elif "glob" in intent_lower or "pattern" in intent_lower:
                return "search_by_name"
            else:
                return "complex_search"
        
        elif operation_type == "terminal":
            if "install" in intent_lower or "package" in intent_lower:
                return "install_packages"
            elif "test" in intent_lower:
                return "test_execution"
            else:
                return "run_commands"
        
        return None
    
    def get_tool_recommendation(self, task_type: str) -> Dict[str, Any]:
        """
        Get tool recommendation details for a task type.
        
        Args:
            task_type: Type of task
            
        Returns:
            Dictionary with tool recommendation details
        """
        if task_type not in self.TASK_TOOL_MAP:
            return {
                "primary": "comprehensive",
                "secondary": [],
                "conditions": "General purpose",
                "tool_set": "comprehensive"
            }
        
        return self.TASK_TOOL_MAP[task_type]


# Global instance
_tool_matrix = None

def get_tool_matrix() -> ToolSelectionMatrix:
    """Get or create the global tool selection matrix instance."""
    global _tool_matrix
    if _tool_matrix is None:
        _tool_matrix = ToolSelectionMatrix()
    return _tool_matrix

