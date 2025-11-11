"""
Output Formatter - Section 10 of Claude Code Plan
Handles output formatting decisions and presentation
"""

from typing import Dict, List, Any, Optional
from enum import Enum


class OutputFormat(Enum):
    """Output format types."""
    CODE = "code"
    MARKDOWN = "markdown"
    TABLE = "table"
    PLAIN = "plain"
    JSON = "json"
    MULTI_FILE = "multi_file"


class OutputFormatter:
    """Handles output formatting following Claude Code logic."""
    
    def __init__(self):
        """Initialize output formatter."""
        pass
    
    def format_output(self, content: Any, format_type: Optional[OutputFormat] = None, context: Optional[Dict] = None) -> str:
        """
        Format output following Section 10.1 logic.
        
        Args:
            content: Content to format
            format_type: Desired format (auto-detected if None)
            context: Optional context
            
        Returns:
            Formatted output string
        """
        # CONTEXT ANALYSIS
        if format_type is None:
            format_type = self._determine_format(content, context)
        
        # Format based on type
        if format_type == OutputFormat.CODE:
            return self._format_code(content, context)
        elif format_type == OutputFormat.MARKDOWN:
            return self._format_markdown(content, context)
        elif format_type == OutputFormat.TABLE:
            return self._format_table(content, context)
        elif format_type == OutputFormat.JSON:
            return self._format_json(content, context)
        elif format_type == OutputFormat.MULTI_FILE:
            return self._format_multi_file(content, context)
        else:
            return self._format_plain(content, context)
    
    def format_error(self, error: Dict[str, Any], context: Optional[Dict] = None) -> str:
        """
        Format error output following Section 10.3 logic.
        
        Args:
            error: Error information
            context: Optional context
            
        Returns:
            Formatted error message
        """
        severity = error.get("severity", "medium")
        message = error.get("error", "Unknown error")
        location = error.get("location", "")
        
        # SEVERITY VISUALIZATION
        if severity == "critical":
            indicator = "❌"
            style = "**CRITICAL ERROR**"
        elif severity == "high":
            indicator = "⚠️"
            style = "**ERROR**"
        else:
            indicator = "ℹ️"
            style = "**WARNING**"
        
        formatted = f"{indicator} {style}\n\n"
        
        # ERROR CONTEXT
        if location:
            formatted += f"**Location:** `{location}`\n\n"
        
        formatted += f"**Message:** {message}\n\n"
        
        # Resolution path
        if "suggestions" in error:
            formatted += "**Suggestions:**\n"
            for suggestion in error["suggestions"]:
                formatted += f"- {suggestion}\n"
        
        return formatted
    
    def _determine_format(self, content: Any, context: Optional[Dict]) -> OutputFormat:
        """Determine output format from context."""
        request_type = context.get("request_type") if context else None
        
        if request_type == "code_generation":
            return OutputFormat.CODE
        elif request_type == "documentation":
            return OutputFormat.MARKDOWN
        elif request_type == "data_display":
            return OutputFormat.TABLE
        elif isinstance(content, (dict, list)):
            return OutputFormat.JSON
        elif isinstance(content, str) and "```" in content:
            return OutputFormat.CODE
        else:
            return OutputFormat.PLAIN
    
    def _format_code(self, content: Any, context: Optional[Dict]) -> str:
        """Format as code block."""
        language = context.get("language", "python") if context else "python"
        
        if isinstance(content, str):
            if content.startswith("```"):
                return content  # Already formatted
            return f"```{language}\n{content}\n```"
        else:
            return f"```{language}\n{str(content)}\n```"
    
    def _format_markdown(self, content: Any, context: Optional[Dict]) -> str:
        """Format as markdown."""
        if isinstance(content, dict):
            # Convert dict to markdown
            md = ""
            for key, value in content.items():
                md += f"## {key}\n\n{value}\n\n"
            return md
        return str(content)
    
    def _format_table(self, content: Any, context: Optional[Dict]) -> str:
        """Format as table."""
        if isinstance(content, list) and content and isinstance(content[0], dict):
            # List of dicts -> table
            headers = list(content[0].keys())
            table = "| " + " | ".join(headers) + " |\n"
            table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for row in content[:20]:  # Limit rows
                values = [str(row.get(h, "")) for h in headers]
                table += "| " + " | ".join(values) + " |\n"
            
            return table
        return str(content)
    
    def _format_json(self, content: Any, context: Optional[Dict]) -> str:
        """Format as JSON."""
        import json
        return json.dumps(content, indent=2)
    
    def _format_multi_file(self, content: Any, context: Optional[Dict]) -> str:
        """Format multi-file output."""
        if isinstance(content, dict):
            output = "# Generated Files\n\n"
            for file_path, file_content in content.items():
                output += f"## {file_path}\n\n"
                output += f"```\n{file_content}\n```\n\n"
            return output
        return str(content)
    
    def _format_plain(self, content: Any, context: Optional[Dict]) -> str:
        """Format as plain text."""
        return str(content)


# Global instance
_output_formatter = None

def get_output_formatter() -> OutputFormatter:
    """Get or create global output formatter."""
    global _output_formatter
    if _output_formatter is None:
        _output_formatter = OutputFormatter()
    return _output_formatter

