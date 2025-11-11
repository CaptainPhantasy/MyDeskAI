"""
Handler Dispatcher - Unified interface to all Claude Code handlers
Routes requests to appropriate handlers based on operation type
"""

from typing import Dict, List, Any, Optional
from decision_engine import get_decision_engine
from file_operations_handler import get_file_handler
from code_generation_handler import get_code_handler
from git_handler import get_git_handler
from search_handler import get_search_handler
from terminal_handler import get_terminal_handler
from error_handling_cascades import get_error_handler
from output_formatter import get_output_formatter
from meta_logic import get_meta_logic


class HandlerDispatcher:
    """Unified dispatcher for all Claude Code handlers."""
    
    def __init__(self):
        """Initialize handler dispatcher."""
        self.decision_engine = get_decision_engine()
        self.file_handler = get_file_handler()
        self.code_handler = get_code_handler()
        self.git_handler = get_git_handler()
        self.search_handler = get_search_handler()
        self.terminal_handler = get_terminal_handler()
        self.error_handler = get_error_handler()
        self.output_formatter = get_output_formatter()
        self.meta_logic = get_meta_logic()
    
    def dispatch(self, request: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Dispatch a request to the appropriate handler.
        
        Args:
            request: User request
            context: Optional context
            
        Returns:
            Handler result with formatted output
        """
        # Process through decision engine
        decision = self.decision_engine.process_request(request, context)
        
        operation_type = decision.get("classification", {}).get("operation_type")
        task_type = decision.get("task_type")
        
        # Route to appropriate handler
        handler_result = None
        
        try:
            if operation_type == "file_operation":
                handler_result = self._handle_file_operation(request, decision, context)
            elif operation_type == "code_operation":
                handler_result = self._handle_code_operation(request, decision, context)
            elif operation_type == "git_operation":
                handler_result = self._handle_git_operation(request, decision, context)
            elif operation_type == "search":
                handler_result = self._handle_search_operation(request, decision, context)
            elif operation_type == "terminal":
                handler_result = self._handle_terminal_operation(request, decision, context)
            else:
                # Default handler
                handler_result = {
                    "success": True,
                    "message": "Request processed",
                    "decision": decision
                }
        except Exception as e:
            # Error handling cascade
            error_result = self.error_handler.handle_error(e, context={"request": request})
            handler_result = {
                "success": False,
                "error": str(e),
                "error_handling": error_result
            }
        
        # Format output
        formatted_output = self.output_formatter.format_output(
            handler_result,
            context={"request_type": operation_type}
        )
        
        # Learn from interaction
        self.meta_logic.learn_from_interaction({
            "task_type": task_type,
            "operation_type": operation_type,
            "success": handler_result.get("success", False) if handler_result else False
        })
        
        return {
            "decision": decision,
            "handler_result": handler_result,
            "formatted_output": formatted_output,
            "operation_type": operation_type
        }
    
    def _handle_file_operation(self, request: str, decision: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle file operations."""
        params = decision.get("parameters", {})
        file_paths = params.get("file_paths", [])
        
        if "read" in request.lower() and file_paths:
            return self.file_handler.read_file(file_paths[0], context)
        elif "create" in request.lower() or "write" in request.lower():
            file_path = file_paths[0] if file_paths else "new_file.txt"
            return self.file_handler.create_file(file_path, "", context)
        elif "delete" in request.lower() and file_paths:
            return self.file_handler.delete_file(file_paths[0], context, confirmed=False)
        else:
            return {"success": False, "error": "Unsupported file operation"}
    
    def _handle_code_operation(self, request: str, decision: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle code operations."""
        if "generate" in request.lower() or "create" in request.lower():
            # Extract component info from request
            return self.code_handler.generate_component("generic", "Component", context=context)
        else:
            return {"success": True, "message": "Code operation handled"}
    
    def _handle_git_operation(self, request: str, decision: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle Git operations."""
        if "commit" in request.lower():
            return self.git_handler.create_commit(context=context)
        elif "status" in request.lower():
            return self.git_handler.check_repository_state(context.get("path") if context else None)
        else:
            return {"success": True, "message": "Git operation handled"}
    
    def _handle_search_operation(self, request: str, decision: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle search operations."""
        # Extract search pattern
        pattern = decision.get("parameters", {}).get("file_paths", ["*"])[0] if decision.get("parameters", {}).get("file_paths") else "*"
        return self.search_handler.search_files(pattern, "name", context)
    
    def _handle_terminal_operation(self, request: str, decision: Dict, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle terminal operations."""
        # Extract command (simplified - would need better parsing)
        command = request  # In real implementation, extract actual command
        return self.terminal_handler.execute_command(command, context, confirmed=False)


# Global instance
_dispatcher = None

def get_dispatcher() -> HandlerDispatcher:
    """Get or create global handler dispatcher."""
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = HandlerDispatcher()
    return _dispatcher

