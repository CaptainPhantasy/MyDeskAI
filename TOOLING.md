# MyDeskAI Tooling Reference

Complete list of all available tools in the MyDeskAI platform, organized by category.

## Currently Integrated Tools

### File Operations
- **FileReadTool** ✅ - Currently integrated in `FileReaderAgent` and `CodeAnalystAgent`
  - Reads and extracts data from files, supporting various file formats (.txt, .csv, .json, etc.)

## Available CrewAI Tools (Not Yet Integrated)

### File & Directory Operations
- **DirectoryReadTool** - Facilitates reading and processing of directory structures and their contents
- **DirectorySearchTool** - RAG tool for searching within directories, useful for navigating file systems
- **FileWriterTool** - Write files to the filesystem
- **FileCompressorTool** - Compress files
- **S3ReaderTool** - Read files from AWS S3
- **S3WriterTool** - Write files to AWS S3

### File Format Search Tools (RAG-based)
- **CSVSearchTool** - RAG tool designed for searching within CSV files
- **DOCXSearchTool** - RAG tool for searching within DOCX documents (Word files)
- **JSONSearchTool** - RAG tool for searching within JSON files
- **MDXSearchTool** - RAG tool for searching within Markdown (MDX) files
- **PDFSearchTool** - RAG tool for searching within PDF documents
- **TXTSearchTool** - RAG tool for searching within text (.txt) files
- **XMLSearchTool** - RAG tool for searching within XML files

### Web Search & Scraping
- **SerperDevTool** - Google search via Serper.dev API
- **SerpApiGoogleSearchTool** - Google search via SerpAPI
- **SerpApiGoogleShoppingTool** - Google Shopping search via SerpAPI
- **BraveSearchTool** - Web search via Brave Search API
- **TavilySearchTool** - Web search via Tavily API
- **TavilyExtractorTool** - Extract structured data from web pages
- **WebsiteSearchTool** - RAG tool for searching website content
- **ScrapeWebsiteTool** - Scrape entire websites
- **ScrapeElementFromWebsiteTool** - Scrape specific elements from websites
- **FirecrawlSearchTool** - Search webpages using Firecrawl
- **FirecrawlCrawlWebsiteTool** - Crawl webpages using Firecrawl
- **FirecrawlScrapeWebsiteTool** - Scrape webpages using Firecrawl
- **JinaScrapeWebsiteTool** - Scrape websites using Jina
- **ScrapflyScrapeWebsiteTool** - Scrape websites using Scrapfly
- **SerperScrapeWebsiteTool** - Scrape websites using Serper
- **ScrapegraphScrapeTool** - Scrape websites using Scrapegraph
- **SeleniumScrapingTool** - Scrape websites using Selenium

### Code & Development
- **CodeInterpreterTool** - Interpret and execute Python code
- **CodeDocsSearchTool** - RAG tool optimized for searching code documentation
- **GithubSearchTool** - RAG tool for searching within GitHub repositories

### Database & Data Sources
- **PGSearchTool** - RAG tool for searching PostgreSQL databases
- **MySQLSearchTool** - Search MySQL databases
- **SingleStoreSearchTool** - Search SingleStore databases
- **SnowflakeSearchTool** - Search Snowflake databases
- **DatabricksQueryTool** - Query Databricks
- **NL2SQLTool** - Natural language to SQL conversion
- **MongoDBVectorSearchTool** - Vector search in MongoDB
- **CouchbaseFTSVectorSearchTool** - Vector search in Couchbase
- **QdrantVectorSearchTool** - Vector search in Qdrant
- **WeaviateVectorSearchTool** - Vector search in Weaviate

### AI & ML Services
- **DallETool** - Generate images using DALL-E API
- **VisionTool** - Vision/image processing capabilities
- **RagTool** - General-purpose RAG tool for various data sources
- **LlamaIndexTool** - Use LlamaIndex tools
- **ContextualAICreateAgentTool** - Create agents via Contextual AI
- **ContextualAIQueryTool** - Query Contextual AI
- **ContextualAIRerankTool** - Rerank results via Contextual AI
- **ContextualAIParseTool** - Parse content via Contextual AI
- **BedrockInvokeAgentTool** - Invoke AWS Bedrock agents
- **BedrockKBRetrieverTool** - Retrieve from AWS Bedrock knowledge bases

### Automation & Integration
- **ComposioTool** - Enable use of Composio tools
- **ZapierActionTool** - Execute Zapier actions
- **MultiOnTool** - MultiOn automation tool
- **StagehandTool** - Stagehand automation tool
- **SpiderTool** - Spider automation tool
- **GenerateCrewaiAutomationTool** - Generate CrewAI automations
- **InvokeCrewAIAutomationTool** - Invoke CrewAI automations
- **EnterpriseActionTool** - Enterprise action tool

### Specialized Search & Data
- **EXASearchTool** - Exhaustive search across various data sources
- **ParallelSearchTool** - Parallel search capabilities
- **ArxivPaperTool** - Search arXiv papers
- **LinkupSearchTool** - Linkup search tool
- **SerplyWebSearchTool** - Web search via Serply
- **SerplyNewsSearchTool** - News search via Serply
- **SerplyScholarSearchTool** - Scholar search via Serply
- **SerplyJobSearchTool** - Job search via Serply
- **SerplyWebpageToMarkdownTool** - Convert webpages to Markdown

### E-commerce & Product Data
- **OxylabsAmazonProductScraperTool** - Scrape Amazon product data
- **OxylabsAmazonSearchScraperTool** - Scrape Amazon search results
- **OxylabsGoogleSearchScraperTool** - Scrape Google search results
- **OxylabsUniversalScraperTool** - Universal scraper via Oxylabs

### Media & Content
- **YoutubeVideoSearchTool** - RAG tool for searching YouTube videos
- **YoutubeChannelSearchTool** - RAG tool for searching YouTube channels
- **OCRTool** - Optical Character Recognition

### Browser & Web Automation
- **BrowserbaseLoadTool** - Interact with web browsers via Browserbase
- **HyperbrowserLoadTool** - Interact with web browsers via Hyperbrowser

### Data & Analytics
- **BrightDataDatasetTool** - Access BrightData datasets
- **BrightDataSearchTool** - Search via BrightData
- **BrightDataWebUnlockerTool** - Web unlocking via BrightData
- **AIMindTool** - AIMind tool

### Evaluation & Testing
- **PatronusEvalTool** - Patronus evaluation tool
- **PatronusLocalEvaluatorTool** - Local Patronus evaluator
- **PatronusPredefinedCriteriaEvalTool** - Predefined criteria evaluator

### Web Scraping Platforms
- **ApifyActorsTool** - Integrate Apify Actors for web scraping and automation

### Model Context Protocol (MCP)
- **MCPServerAdapter** - Connect to MCP servers for extended capabilities

## Tool Categories Summary

| Category | Count | Examples |
|----------|-------|----------|
| **File Operations** | 6 | FileReadTool, DirectoryReadTool, FileWriterTool |
| **Web Search** | 8 | SerperDevTool, BraveSearchTool, TavilySearchTool |
| **Web Scraping** | 12 | ScrapeWebsiteTool, FirecrawlScrapeWebsiteTool, SeleniumScrapingTool |
| **Database** | 9 | PGSearchTool, MongoDBVectorSearchTool, SnowflakeSearchTool |
| **Code & Dev** | 3 | CodeInterpreterTool, CodeDocsSearchTool, GithubSearchTool |
| **AI/ML Services** | 9 | DallETool, VisionTool, RagTool, LlamaIndexTool |
| **Automation** | 7 | ComposioTool, ZapierActionTool, MultiOnTool |
| **Media** | 3 | YoutubeVideoSearchTool, YoutubeChannelSearchTool, OCRTool |
| **Specialized** | 15+ | ArxivPaperTool, EXASearchTool, Various scrapers |

## Integration Status

### ✅ Phase 3 (Current)
- **FileReadTool** - Integrated in FileReaderAgent and CodeAnalystAgent

### 🔄 Recommended Next Integrations
1. **DirectoryReadTool** - For reading entire directories
2. **CodeInterpreterTool** - For executing Python code
3. **GithubSearchTool** - For searching GitHub repos
4. **SerperDevTool** - For web search capabilities
5. **WebsiteSearchTool** - For RAG-based web content search

### 📋 Future Considerations
- Database tools (PGSearchTool, MongoDBVectorSearchTool)
- Advanced scraping tools (Firecrawl, Selenium)
- AI services (DallETool, VisionTool)
- Automation tools (ComposioTool, ZapierActionTool)

## Usage Notes

- All tools support **error handling** and **caching** by default
- Tools can be **asynchronously** executed for better performance
- Custom tools can be created by subclassing `BaseTool` from `crewai.tools`
- Tools are assigned to agents via the `tools` parameter in the Agent constructor
- Some tools require API keys (configured in `.env` or via environment variables)

## Adding New Tools

To add a new tool to an agent:

```python
from crewai_tools import YourTool

agent = Agent(
    role="Your Role",
    goal="Your Goal",
    backstory="Your Backstory",
    tools=[YourTool()],  # Add tool here
    llm=llm_wrapper,
)
```

## Documentation

- Full tool documentation: `/repos/crewai/docs/en/concepts/tools.mdx`
- Tool source code: `/repos/crewai/lib/crewai/src/crewai/tools/`
- CrewAI Tools package: https://github.com/joaomdmoura/crewai-tools

