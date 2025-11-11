"""
Tools Registry - Comprehensive tool organization for MyDeskAI
Imports and organizes all available crewai_tools for intelligent agent assignment.
Includes LangChain shell tools for BASH, GREP, and GLOB operations.

Reference: https://github.com/crewAIInc/crewAI-tools
"""

from typing import List, Dict, Any, Optional
import warnings

# Import LangChain shell tools for BASH, GREP, GLOB
try:
    from langchain_community.tools import ShellTool
    SHELL_TOOL_AVAILABLE = True
except ImportError:
    ShellTool = None
    SHELL_TOOL_AVAILABLE = False
    warnings.warn("ShellTool not available. Install langchain-community for shell access.")

# Import all crewai_tools
from crewai_tools import (
    # File Operations
    FileReadTool,
    FileWriterTool,
    DirectoryReadTool,
    DirectorySearchTool,
    FileCompressorTool,
    
    # File Format Search (RAG)
    CSVSearchTool,
    DOCXSearchTool,
    JSONSearchTool,
    MDXSearchTool,
    PDFSearchTool,
    TXTSearchTool,
    XMLSearchTool,
    
    # Web Search
    SerperDevTool,
    SerpApiGoogleSearchTool,
    SerpApiGoogleShoppingTool,
    BraveSearchTool,
    TavilySearchTool,
    TavilyExtractorTool,
    WebsiteSearchTool,
    SerplyWebSearchTool,
    SerplyNewsSearchTool,
    SerplyScholarSearchTool,
    SerplyJobSearchTool,
    SerplyWebpageToMarkdownTool,
    
    # Web Scraping
    ScrapeWebsiteTool,
    ScrapeElementFromWebsiteTool,
    FirecrawlSearchTool,
    FirecrawlCrawlWebsiteTool,
    FirecrawlScrapeWebsiteTool,
    JinaScrapeWebsiteTool,
    ScrapflyScrapeWebsiteTool,
    SerperScrapeWebsiteTool,
    ScrapegraphScrapeTool,
    SeleniumScrapingTool,
    
    # Code & Development
    CodeInterpreterTool,
    CodeDocsSearchTool,
    GithubSearchTool,
    
    # Database & Data Sources
    MySQLSearchTool,
    SingleStoreSearchTool,
    SnowflakeSearchTool,
    DatabricksQueryTool,
    NL2SQLTool,
    MongoDBVectorSearchTool,
    CouchbaseFTSVectorSearchTool,
    QdrantVectorSearchTool,
    WeaviateVectorSearchTool,
    
    # AI/ML Services
    DallETool,
    VisionTool,
    RagTool,
    LlamaIndexTool,
    ContextualAICreateAgentTool,
    ContextualAIQueryTool,
    ContextualAIRerankTool,
    ContextualAIParseTool,
    
    # Automation & Integration
    ComposioTool,
    ZapierActionTool,
    MultiOnTool,
    StagehandTool,
    SpiderTool,
    GenerateCrewaiAutomationTool,
    InvokeCrewAIAutomationTool,
    
    # Media & Content
    YoutubeVideoSearchTool,
    YoutubeChannelSearchTool,
    OCRTool,
    
    # Specialized Search
    EXASearchTool,
    ParallelSearchTool,
    ArxivPaperTool,
    LinkupSearchTool,
    
    # E-commerce & Product Data
    OxylabsAmazonProductScraperTool,
    OxylabsAmazonSearchScraperTool,
    OxylabsGoogleSearchScraperTool,
    OxylabsUniversalScraperTool,
    
    # Browser & Web Automation
    BrowserbaseLoadTool,
    HyperbrowserLoadTool,
    
    # Data & Analytics
    BrightDataDatasetTool,
    BrightDataSearchTool,
    BrightDataWebUnlockerTool,
    AIMindTool,
    
    # Evaluation & Testing
    PatronusEvalTool,
    PatronusLocalEvaluatorTool,
    PatronusPredefinedCriteriaEvalTool,
    
    # Web Scraping Platforms
    ApifyActorsTool,
)

# Import optional tools with graceful fallback
try:
    from crewai_tools.aws.s3 import S3ReaderTool, S3WriterTool
    S3_TOOLS_AVAILABLE = True
except ImportError:
    S3ReaderTool = None
    S3WriterTool = None
    S3_TOOLS_AVAILABLE = False

try:
    from crewai_tools.adapters.mcp_adapter import MCPServerAdapter
    MCP_AVAILABLE = True
except ImportError:
    MCPServerAdapter = None
    MCP_AVAILABLE = False

# Tool Categories
TOOL_CATEGORIES = {
    "file_operations": {
        "name": "File Operations",
        "tools": [FileReadTool, FileWriterTool, DirectoryReadTool, DirectorySearchTool, FileCompressorTool] + ([S3ReaderTool, S3WriterTool] if S3_TOOLS_AVAILABLE else []),
        "description": "Tools for reading, writing, and managing files and directories",
    },
    "shell_operations": {
        "name": "Shell Operations (BASH, GREP, GLOB)",
        "tools": [ShellTool] if SHELL_TOOL_AVAILABLE else [],
        "description": "LangChain ShellTool for executing shell commands, grep, glob patterns, and bash operations",
    },
    "file_format_search": {
        "name": "File Format Search (RAG)",
        "tools": [CSVSearchTool, DOCXSearchTool, JSONSearchTool, MDXSearchTool, PDFSearchTool, TXTSearchTool, XMLSearchTool],
        "description": "RAG-based search tools for specific file formats",
    },
    "web_search": {
        "name": "Web Search",
        "tools": [SerperDevTool, SerpApiGoogleSearchTool, SerpApiGoogleShoppingTool, BraveSearchTool, TavilySearchTool, TavilyExtractorTool, WebsiteSearchTool, SerplyWebSearchTool, SerplyNewsSearchTool, SerplyScholarSearchTool, SerplyJobSearchTool, SerplyWebpageToMarkdownTool],
        "description": "Tools for searching the web and extracting information",
    },
    "web_scraping": {
        "name": "Web Scraping",
        "tools": [ScrapeWebsiteTool, ScrapeElementFromWebsiteTool, FirecrawlSearchTool, FirecrawlCrawlWebsiteTool, FirecrawlScrapeWebsiteTool, JinaScrapeWebsiteTool, ScrapflyScrapeWebsiteTool, SerperScrapeWebsiteTool, ScrapegraphScrapeTool, SeleniumScrapingTool],
        "description": "Tools for scraping and extracting data from websites",
    },
    "code_development": {
        "name": "Code & Development",
        "tools": [CodeInterpreterTool, CodeDocsSearchTool, GithubSearchTool],
        "description": "Tools for code execution, documentation search, and GitHub integration",
    },
    "database": {
        "name": "Database & Data Sources",
        "tools": [MySQLSearchTool, SingleStoreSearchTool, SnowflakeSearchTool, DatabricksQueryTool, NL2SQLTool, MongoDBVectorSearchTool, CouchbaseFTSVectorSearchTool, QdrantVectorSearchTool, WeaviateVectorSearchTool],
        "description": "Tools for querying databases and vector stores",
    },
    "ai_ml_services": {
        "name": "AI/ML Services",
        "tools": [DallETool, VisionTool, RagTool, LlamaIndexTool, ContextualAICreateAgentTool, ContextualAIQueryTool, ContextualAIRerankTool, ContextualAIParseTool],
        "description": "AI and ML service integrations",
    },
    "automation": {
        "name": "Automation & Integration",
        "tools": [ComposioTool, ZapierActionTool, MultiOnTool, StagehandTool, SpiderTool, GenerateCrewaiAutomationTool, InvokeCrewAIAutomationTool],
        "description": "Tools for workflow automation and integrations",
    },
    "media": {
        "name": "Media & Content",
        "tools": [YoutubeVideoSearchTool, YoutubeChannelSearchTool, OCRTool],
        "description": "Tools for media content and OCR",
    },
    "specialized": {
        "name": "Specialized Tools",
        "tools": [EXASearchTool, ParallelSearchTool, ArxivPaperTool, LinkupSearchTool, OxylabsAmazonProductScraperTool, OxylabsAmazonSearchScraperTool, OxylabsGoogleSearchScraperTool, OxylabsUniversalScraperTool, BrowserbaseLoadTool, HyperbrowserLoadTool, BrightDataDatasetTool, BrightDataSearchTool, BrightDataWebUnlockerTool, AIMindTool, PatronusEvalTool, PatronusLocalEvaluatorTool, PatronusPredefinedCriteriaEvalTool, ApifyActorsTool] + ([MCPServerAdapter] if MCP_AVAILABLE else []),
        "description": "Specialized tools for specific use cases",
    },
}

# Pre-configured Tool Sets for Common Use Cases (lazy-loaded to avoid optional dependency issues)
TOOL_SETS = {
    "file_operations": {
        "name": "File Operations Set",
        "tool_classes": [FileReadTool, FileWriterTool, DirectoryReadTool],
        "use_cases": ["Reading files", "Writing files", "Directory operations"],
    },
    "shell_operations": {
        "name": "Shell Operations Set (BASH, GREP, GLOB)",
        "tool_classes": [ShellTool] if SHELL_TOOL_AVAILABLE else [],
        "use_cases": ["Shell commands", "grep operations", "glob patterns", "bash scripting"],
    },
    "code_analysis": {
        "name": "Code Analysis Set",
        "tool_classes": [FileReadTool, CodeInterpreterTool, CodeDocsSearchTool, GithubSearchTool],
        "use_cases": ["Code review", "Code analysis", "Documentation search"],
    },
    "web_research": {
        "name": "Web Research Set",
        "tool_classes": [SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool, TavilySearchTool],
        "use_cases": ["Web research", "Information gathering", "Content extraction"],
    },
    "comprehensive": {
        "name": "Comprehensive Set",
        "tool_classes": [FileReadTool, FileWriterTool, DirectoryReadTool, SerperDevTool, CodeInterpreterTool, WebsiteSearchTool, GithubSearchTool] + ([ShellTool] if SHELL_TOOL_AVAILABLE else []),
        "use_cases": ["General purpose", "Multi-domain tasks"],
    },
    "minimal": {
        "name": "Minimal Set",
        "tool_classes": [FileReadTool],
        "use_cases": ["Basic file operations"],
    },
}


def get_tools_by_category(category: str) -> List[Any]:
    """Get all tools in a specific category."""
    if category in TOOL_CATEGORIES:
        return [tool for tool in TOOL_CATEGORIES[category]["tools"] if tool is not None]
    return []


def get_tool_set(set_name: str) -> List[Any]:
    """Get a pre-configured tool set (lazy-loaded to avoid optional dependency issues)."""
    if set_name in TOOL_SETS:
        tool_classes = TOOL_SETS[set_name].get("tool_classes", [])
        tools = []
        for tool_class in tool_classes:
            if tool_class is not None:
                try:
                    tools.append(tool_class())
                except Exception as e:
                    warnings.warn(f"Could not instantiate {tool_class.__name__}: {e}")
        return tools
    return []


def get_all_tools() -> List[Any]:
    """Get all available tools."""
    all_tools = []
    for category in TOOL_CATEGORIES.values():
        all_tools.extend([tool for tool in category["tools"] if tool is not None])
    return all_tools


def get_tool_by_name(tool_name: str) -> Optional[Any]:
    """Get a specific tool class by name."""
    for category in TOOL_CATEGORIES.values():
        for tool in category["tools"]:
            if tool is not None and tool.__name__ == tool_name:
                return tool
    return None


def list_all_tool_names() -> List[str]:
    """List all available tool names."""
    return [tool.__name__ for tool in get_all_tools() if tool is not None]


def get_category_info() -> Dict[str, Dict[str, Any]]:
    """Get information about all categories."""
    return {
        cat_id: {
            "name": info["name"],
            "count": len([t for t in info["tools"] if t is not None]),
            "description": info["description"],
            "tools": [tool.__name__ for tool in info["tools"] if tool is not None],
        }
        for cat_id, info in TOOL_CATEGORIES.items()
    }
