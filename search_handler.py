"""
Search Handler - Section 7 of Claude Code Plan
Handles file search, code search, and analysis
"""

import os
import re
import glob
from typing import Dict, List, Any, Optional
from pathlib import Path
from tools_registry import DirectorySearchTool, FileReadTool


class SearchHandler:
    """Handles search operations following Claude Code logic."""
    
    def __init__(self):
        """Initialize search handler."""
        try:
            self.directory_search = DirectorySearchTool()
        except Exception:
            self.directory_search = None  # Optional dependency
        self.file_read = FileReadTool()
    
    def search_files(self, pattern: str, search_type: str = "name", context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Search for files following Section 7.1 logic.
        
        Args:
            pattern: Search pattern
            search_type: Type of search (name, content, type)
            context: Optional context
            
        Returns:
            Search results
        """
        search_path = context.get("current_directory") if context else os.getcwd()
        
        # SEARCH TYPE DETERMINATION
        if search_type == "name" or "glob" in pattern.lower():
            # Use Glob tool
            return self._search_by_name(pattern, search_path)
        elif search_type == "content" or "grep" in pattern.lower():
            # Use Grep tool
            return self._search_by_content(pattern, search_path)
        elif search_type == "type":
            # Search by extension
            return self._search_by_type(pattern, search_path)
        else:
            # Exploratory search
            return self._exploratory_search(pattern, search_path)
    
    def analyze_code(self, file_path: str, analysis_type: str = "structure", context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze code following Section 7.2 logic.
        
        Args:
            file_path: Path to code file
            analysis_type: Type of analysis (structure, quality, performance)
            context: Optional context
            
        Returns:
            Analysis results
        """
        # Read file
        read_result = self.file_read._run(file_path)
        if not read_result:
            return {
                "success": False,
                "error": "Could not read file"
            }
        
        content = read_result if isinstance(read_result, str) else str(read_result)
        
        # ANALYSIS TYPE
        if analysis_type == "structure":
            return self._analyze_structure(content, file_path)
        elif analysis_type == "quality":
            return self._analyze_quality(content, file_path)
        elif analysis_type == "performance":
            return self._analyze_performance(content, file_path)
        else:
            return self._analyze_structure(content, file_path)
    
    def _search_by_name(self, pattern: str, search_path: str) -> Dict[str, Any]:
        """Search files by name using glob."""
        try:
            # Convert pattern to glob format
            if not pattern.startswith("*"):
                pattern = f"**/{pattern}"
            
            matches = list(Path(search_path).rglob(pattern))
            
            # Filter out common exclusions
            excluded = {".git", "node_modules", "__pycache__", ".venv", "venv"}
            matches = [m for m in matches if not any(exc in str(m) for exc in excluded)]
            
            return {
                "success": True,
                "search_type": "name",
                "pattern": pattern,
                "matches": [str(m) for m in matches[:50]],  # Limit to 50
                "count": len(matches)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _search_by_content(self, pattern: str, search_path: str) -> Dict[str, Any]:
        """Search files by content using grep-like search."""
        matches = []
        
        try:
            # Search in Python files
            for py_file in Path(search_path).rglob("*.py"):
                if any(exc in str(py_file) for exc in [".git", "node_modules", "__pycache__"]):
                    continue
                
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(pattern, content, re.IGNORECASE):
                            # Find line numbers
                            lines = content.splitlines()
                            matching_lines = [
                                (i+1, line) for i, line in enumerate(lines)
                                if re.search(pattern, line, re.IGNORECASE)
                            ]
                            matches.append({
                                "file": str(py_file),
                                "matches": matching_lines[:10]  # Limit per file
                            })
                except Exception:
                    continue
                
                if len(matches) >= 20:  # Limit total results
                    break
            
            return {
                "success": True,
                "search_type": "content",
                "pattern": pattern,
                "matches": matches,
                "count": len(matches)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _search_by_type(self, extension: str, search_path: str) -> Dict[str, Any]:
        """Search files by type/extension."""
        if not extension.startswith("."):
            extension = f".{extension}"
        
        pattern = f"**/*{extension}"
        return self._search_by_name(pattern, search_path)
    
    def _exploratory_search(self, query: str, search_path: str) -> Dict[str, Any]:
        """Perform exploratory search."""
        # Try multiple search strategies
        name_results = self._search_by_name(f"*{query}*", search_path)
        content_results = self._search_by_content(query, search_path)
        
        return {
            "success": True,
            "search_type": "exploratory",
            "query": query,
            "name_matches": name_results.get("matches", []),
            "content_matches": content_results.get("matches", []),
            "total": name_results.get("count", 0) + len(content_results.get("matches", []))
        }
    
    def _analyze_structure(self, content: str, file_path: str) -> Dict[str, Any]:
        """Analyze code structure."""
        lines = content.splitlines()
        
        # Find functions
        functions = re.findall(r'def\s+(\w+)\s*\(', content)
        
        # Find classes
        classes = re.findall(r'class\s+(\w+)', content)
        
        # Find imports
        imports = re.findall(r'^(?:from|import)\s+[\w.]+', content, re.MULTILINE)
        
        return {
            "success": True,
            "analysis_type": "structure",
            "file": file_path,
            "lines": len(lines),
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": "low" if len(functions) < 10 else "medium" if len(functions) < 30 else "high"
        }
    
    def _analyze_quality(self, content: str, file_path: str) -> Dict[str, Any]:
        """Analyze code quality."""
        structure = self._analyze_structure(content, file_path)
        
        # Check for docstrings
        has_docstrings = bool(re.search(r'""".*"""', content, re.DOTALL))
        
        # Check for error handling
        has_error_handling = bool(re.search(r'try:', content))
        
        # Check line length (basic)
        long_lines = sum(1 for line in content.splitlines() if len(line) > 100)
        
        return {
            **structure,
            "analysis_type": "quality",
            "has_docstrings": has_docstrings,
            "has_error_handling": has_error_handling,
            "long_lines": long_lines,
            "quality_score": self._calculate_quality_score(has_docstrings, has_error_handling, long_lines)
        }
    
    def _analyze_performance(self, content: str, file_path: str) -> Dict[str, Any]:
        """Analyze code performance."""
        structure = self._analyze_structure(content, file_path)
        
        # Check for potential performance issues
        nested_loops = len(re.findall(r'for\s+.*:\s*\n\s*for\s+', content))
        recursive_calls = len(re.findall(r'\w+\s*\(.*\w+\(', content))
        
        return {
            **structure,
            "analysis_type": "performance",
            "nested_loops": nested_loops,
            "recursive_calls": recursive_calls,
            "performance_concerns": nested_loops > 2 or recursive_calls > 5
        }
    
    def _calculate_quality_score(self, has_docstrings: bool, has_error_handling: bool, long_lines: int) -> float:
        """Calculate quality score."""
        score = 0.0
        if has_docstrings:
            score += 0.3
        if has_error_handling:
            score += 0.3
        if long_lines == 0:
            score += 0.4
        elif long_lines < 5:
            score += 0.2
        
        return min(1.0, score)


# Global instance
_search_handler = None

def get_search_handler() -> SearchHandler:
    """Get or create global search handler."""
    global _search_handler
    if _search_handler is None:
        _search_handler = SearchHandler()
    return _search_handler

