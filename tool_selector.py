"""
Tool Selector - Intelligent tool selection based on user prompts
Uses COT (Chain of Thought) reasoning to match prompts to appropriate tools.
"""

from typing import List, Dict, Any, Optional
import re
from tools_registry import (
    get_tool_set,
    get_tools_by_category,
    TOOL_CATEGORIES,
    TOOL_SETS,
    SHELL_TOOL_AVAILABLE,
)


class ToolSelector:
    """
    Intelligently selects tools based on user prompts using keyword matching
    and semantic analysis.
    """
    
    # Keyword mappings for tool categories
    KEYWORD_MAPPINGS = {
        "file_operations": [
            "read", "file", "write", "directory", "folder", "save", "load",
            ".py", ".md", ".txt", ".json", ".csv", ".yaml", ".yml",
            "filepath", "path", "open", "create", "delete", "edit"
        ],
        "shell_operations": [
            "bash", "shell", "command", "grep", "glob", "terminal", "cli",
            "execute", "run", "find", "search", "pattern", "regex"
        ],
        "file_format_search": [
            "search in", "find in", "csv", "pdf", "docx", "json", "xml",
            "markdown", "mdx", "txt", "within file"
        ],
        "web_search": [
            "search", "google", "find information", "lookup", "research",
            "web", "internet", "online", "news", "scholar", "job"
        ],
        "web_scraping": [
            "scrape", "crawl", "extract", "website", "url", "html",
            "webpage", "download", "fetch"
        ],
        "code_development": [
            "code", "programming", "function", "class", "github", "repo",
            "repository", "debug", "execute code", "python", "javascript"
        ],
        "database": [
            "database", "query", "sql", "mysql", "postgres", "mongodb",
            "vector", "search database", "db"
        ],
        "ai_ml_services": [
            "image", "generate", "dall-e", "vision", "rag", "embedding",
            "llm", "model", "ai service"
        ],
        "automation": [
            "automate", "workflow", "zapier", "composio", "integration",
            "api", "webhook"
        ],
        "media": [
            "youtube", "video", "channel", "ocr", "image", "picture",
            "photo", "media"
        ],
    }
    
    def __init__(self):
        """Initialize the tool selector."""
        self.prompt_cache = {}
    
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze a prompt and determine which tool categories are needed.
        
        Args:
            prompt: User's prompt/request
            
        Returns:
            Dictionary with analysis results including matched categories and confidence scores
        """
        prompt_lower = prompt.lower()
        
        # Count keyword matches per category
        category_scores = {}
        for category, keywords in self.KEYWORD_MAPPINGS.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                category_scores[category] = score
        
        # Determine primary category (highest score)
        primary_category = None
        if category_scores:
            primary_category = max(category_scores, key=category_scores.get)
        
        # Check for file extensions
        file_extensions = re.findall(r'\.\w+', prompt_lower)
        if file_extensions:
            category_scores["file_operations"] = category_scores.get("file_operations", 0) + len(file_extensions)
            if not primary_category:
                primary_category = "file_operations"
        
        # Check for explicit tool mentions
        explicit_tools = []
        for category in TOOL_CATEGORIES.keys():
            if category in prompt_lower:
                category_scores[category] = category_scores.get(category, 0) + 5
                if not primary_category:
                    primary_category = category
        
        return {
            "primary_category": primary_category,
            "category_scores": category_scores,
            "matched_categories": list(category_scores.keys()),
            "confidence": max(category_scores.values()) if category_scores else 0,
        }
    
    def select_tools(self, prompt: str, max_tools: int = 5) -> List[Any]:
        """
        Select appropriate tools based on prompt analysis.
        
        Args:
            prompt: User's prompt/request
            max_tools: Maximum number of tools to return
            
        Returns:
            List of tool instances
        """
        analysis = self.analyze_prompt(prompt)
        
        tools = []
        
        # If we have a high-confidence primary category, use a specific tool set
        if analysis["confidence"] >= 3 and analysis["primary_category"]:
            category = analysis["primary_category"]
            
            # Map categories to tool sets
            category_to_set = {
                "file_operations": "file_operations",
                "shell_operations": "shell_operations",
                "code_development": "code_analysis",
                "web_search": "web_research",
            }
            
            set_name = category_to_set.get(category)
            if set_name:
                tools = get_tool_set(set_name)
        
        # If no specific set or low confidence, use comprehensive set
        if not tools:
            tools = get_tool_set("comprehensive")
        
        # Limit to max_tools
        return tools[:max_tools]
    
    def select_tools_by_category(self, category: str) -> List[Any]:
        """
        Select tools from a specific category.
        
        Args:
            category: Tool category name
            
        Returns:
            List of tool instances
        """
        tool_classes = get_tools_by_category(category)
        tools = []
        for tool_class in tool_classes[:5]:  # Limit to 5 tools
            if tool_class is not None:
                try:
                    tools.append(tool_class())
                except Exception as e:
                    pass  # Skip tools that can't be instantiated
        return tools
    
    def get_recommended_tool_set(self, prompt: str) -> str:
        """
        Get the name of the recommended tool set for a prompt.
        
        Args:
            prompt: User's prompt/request
            
        Returns:
            Name of recommended tool set
        """
        analysis = self.analyze_prompt(prompt)
        
        if analysis["confidence"] >= 3 and analysis["primary_category"]:
            category = analysis["primary_category"]
            category_to_set = {
                "file_operations": "file_operations",
                "shell_operations": "shell_operations",
                "code_development": "code_analysis",
                "web_search": "web_research",
            }
            return category_to_set.get(category, "comprehensive")
        
        return "comprehensive"


# Global instance
_tool_selector = None

def get_tool_selector() -> ToolSelector:
    """Get or create the global tool selector instance."""
    global _tool_selector
    if _tool_selector is None:
        _tool_selector = ToolSelector()
    return _tool_selector

