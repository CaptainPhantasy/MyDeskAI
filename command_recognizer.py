"""
Command Recognizer - Core command recognition and decision framework
Implements Section 1 of Claude Code Comprehensive Logic Plan
"""

from typing import Dict, List, Any, Optional, Tuple
import re
from enum import Enum


class IntentType(Enum):
    """Types of user intents."""
    EXPLICIT_COMMAND = "explicit"
    IMPLICIT_REQUEST = "implicit"
    AMBIGUOUS = "ambiguous"
    INITIALIZATION = "init"
    GENERATION = "generation"
    DEBUGGING = "debugging"
    TESTING = "testing"
    FILE_OPERATION = "file_operation"
    CODE_OPERATION = "code_operation"
    GIT_OPERATION = "git_operation"
    SEARCH = "search"
    TERMINAL = "terminal"


class CommandRecognizer:
    """
    Recognizes and classifies user commands using the Claude Code logic framework.
    """
    
    # Explicit command patterns
    EXPLICIT_PATTERNS = {
        "create": r"\b(create|make|new|add)\s+",
        "read": r"\b(read|show|display|view|open|cat)\s+",
        "write": r"\b(write|save|update|modify|edit|change)\s+",
        "delete": r"\b(delete|remove|rm|del)\s+",
        "run": r"\b(run|execute|start|launch)\s+",
        "test": r"\b(test|spec|check)\s+",
        "init": r"\b(init|initialize|setup|bootstrap)\s+",
        "fix": r"\b(fix|debug|repair|resolve)\s+",
    }
    
    # Implicit request patterns
    IMPLICIT_PATTERNS = {
        "need": r"\b(need|want|require|should have)\s+",
        "problem": r"\b(problem|issue|error|bug|broken|not working)\s+",
        "improve": r"\b(improve|better|optimize|enhance|refactor)\s+",
        "add": r"\b(add|implement|include)\s+",
    }
    
    # File operation indicators
    FILE_INDICATORS = [
        "file", "directory", "folder", "path", ".py", ".js", ".ts", ".md",
        ".json", ".yaml", ".yml", ".txt", ".csv", "read", "write", "save"
    ]
    
    # Code operation indicators
    CODE_INDICATORS = [
        "code", "function", "class", "method", "component", "module",
        "programming", "implement", "generate", "create", "build"
    ]
    
    # Git operation indicators
    GIT_INDICATORS = [
        "git", "commit", "push", "pull", "branch", "merge", "rebase",
        "stash", "tag", "remote", "repository", "repo"
    ]
    
    # Search indicators
    SEARCH_INDICATORS = [
        "search", "find", "grep", "glob", "look for", "locate",
        "where is", "show me", "list"
    ]
    
    def __init__(self):
        """Initialize the command recognizer."""
        self.command_history = []
    
    def classify_input(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Classify user input according to Claude Code logic framework.
        
        Args:
            user_input: The user's input string
            context: Optional context (current directory, project type, etc.)
            
        Returns:
            Classification result with intent, confidence, and metadata
        """
        input_lower = user_input.lower().strip()
        
        # Character analysis
        starts_with_slash = input_lower.startswith('/')
        
        # Intent classification
        intent = self._determine_intent(input_lower, starts_with_slash)
        
        # Confidence scoring
        confidence = self._calculate_confidence(input_lower, intent)
        
        # Operation type detection
        operation_type = self._detect_operation_type(input_lower)
        
        # Context evaluation
        context_info = self._evaluate_context(input_lower, context)
        
        result = {
            "intent": intent,
            "confidence": confidence,
            "operation_type": operation_type,
            "input": user_input,
            "context": context_info,
            "requires_clarification": confidence < 0.4,
            "routing": self._determine_routing(confidence),
        }
        
        self.command_history.append(result)
        return result
    
    def _determine_intent(self, input_lower: str, starts_with_slash: bool) -> IntentType:
        """Determine the primary intent of the input."""
        if starts_with_slash:
            return IntentType.EXPLICIT_COMMAND
        
        # Check explicit patterns
        for pattern in self.EXPLICIT_PATTERNS.values():
            if re.search(pattern, input_lower):
                return IntentType.EXPLICIT_COMMAND
        
        # Check implicit patterns
        for pattern in self.IMPLICIT_PATTERNS.values():
            if re.search(pattern, input_lower):
                return IntentType.IMPLICIT_REQUEST
        
        # Check specific intents
        if "init" in input_lower or "initialize" in input_lower or "setup" in input_lower:
            return IntentType.INITIALIZATION
        
        if any(word in input_lower for word in ["create", "generate", "make", "new"]):
            return IntentType.GENERATION
        
        if any(word in input_lower for word in ["fix", "debug", "error", "bug"]):
            return IntentType.DEBUGGING
        
        if any(word in input_lower for word in ["test", "spec", "check"]):
            return IntentType.TESTING
        
        # Default to ambiguous if unclear
        return IntentType.AMBIGUOUS
    
    def _calculate_confidence(self, input_lower: str, intent: IntentType) -> float:
        """Calculate confidence score for the classification."""
        if intent == IntentType.EXPLICIT_COMMAND:
            return 1.0
        
        if intent == IntentType.AMBIGUOUS:
            return 0.3
        
        # Count matching patterns
        explicit_matches = sum(1 for pattern in self.EXPLICIT_PATTERNS.values() 
                             if re.search(pattern, input_lower))
        implicit_matches = sum(1 for pattern in self.IMPLICIT_PATTERNS.values() 
                              if re.search(pattern, input_lower))
        
        if explicit_matches > 0:
            return min(0.8, 0.6 + (explicit_matches * 0.1))
        
        if implicit_matches > 0:
            return min(0.6, 0.4 + (implicit_matches * 0.1))
        
        return 0.5
    
    def _detect_operation_type(self, input_lower: str) -> Optional[str]:
        """Detect the type of operation requested."""
        # File operations
        if any(indicator in input_lower for indicator in self.FILE_INDICATORS):
            return "file_operation"
        
        # Code operations
        if any(indicator in input_lower for indicator in self.CODE_INDICATORS):
            return "code_operation"
        
        # Git operations
        if any(indicator in input_lower for indicator in self.GIT_INDICATORS):
            return "git_operation"
        
        # Search operations
        if any(indicator in input_lower for indicator in self.SEARCH_INDICATORS):
            return "search"
        
        # Terminal operations
        if any(word in input_lower for word in ["run", "execute", "command", "bash", "shell"]):
            return "terminal"
        
        return None
    
    def _evaluate_context(self, input_lower: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate context for the command."""
        context_info = {
            "has_context": context is not None,
            "current_directory": context.get("current_directory") if context else None,
            "project_type": context.get("project_type") if context else None,
            "recent_operations": context.get("recent_operations", []) if context else [],
        }
        
        # Detect file extensions in input
        file_extensions = re.findall(r'\.\w+', input_lower)
        context_info["file_extensions"] = file_extensions
        
        # Detect paths
        paths = re.findall(r'[\w/\\]+\.\w+', input_lower)
        context_info["detected_paths"] = paths
        
        return context_info
    
    def _determine_routing(self, confidence: float) -> str:
        """Determine how to route the command based on confidence."""
        if confidence >= 0.8:
            return "execute_immediately"
        elif confidence >= 0.5:
            return "confirm_with_preview"
        else:
            return "present_options_menu"
    
    def extract_parameters(self, user_input: str, intent: IntentType) -> Dict[str, Any]:
        """Extract parameters from the user input."""
        params = {}
        input_lower = user_input.lower()
        
        # Extract file paths
        file_paths = re.findall(r'[\w/\\]+\.\w+', user_input)
        if file_paths:
            params["file_paths"] = file_paths
        
        # Extract directory paths
        dir_paths = re.findall(r'[\w/\\]+/', user_input)
        if dir_paths:
            params["directory_paths"] = dir_paths
        
        # Extract file extensions
        extensions = re.findall(r'\.\w+', input_lower)
        if extensions:
            params["file_extensions"] = list(set(extensions))
        
        # Extract command names (for explicit commands)
        if intent == IntentType.EXPLICIT_COMMAND:
            for cmd, pattern in self.EXPLICIT_PATTERNS.items():
                if re.search(pattern, input_lower):
                    params["command"] = cmd
                    break
        
        return params


# Global instance
_command_recognizer = None

def get_command_recognizer() -> CommandRecognizer:
    """Get or create the global command recognizer instance."""
    global _command_recognizer
    if _command_recognizer is None:
        _command_recognizer = CommandRecognizer()
    return _command_recognizer

