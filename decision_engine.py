"""
Decision Engine - Implements Claude Code decision trees and routing logic
Combines command recognition with tool selection for intelligent routing
"""

from typing import Dict, List, Any, Optional
from command_recognizer import get_command_recognizer, IntentType
from tool_selection_matrix import get_tool_matrix
from tool_selector import get_tool_selector


class DecisionEngine:
    """
    Main decision engine that routes commands to appropriate handlers
    based on Claude Code comprehensive logic plan.
    """
    
    def __init__(self):
        """Initialize the decision engine."""
        self.command_recognizer = get_command_recognizer()
        self.tool_matrix = get_tool_matrix()
        self.tool_selector = get_tool_selector()
    
    def process_request(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user request through the complete decision pipeline.
        
        Args:
            user_input: User's input/request
            context: Optional context (directory, project type, etc.)
            
        Returns:
            Complete decision result with routing, tools, and execution plan
        """
        # Step 1: Command Recognition
        classification = self.command_recognizer.classify_input(user_input, context)
        
        # Step 2: Extract Parameters
        params = self.command_recognizer.extract_parameters(
            user_input, 
            classification["intent"]
        )
        
        # Step 3: Determine Task Type
        task_type = self.tool_matrix.get_task_type_from_operation(
            classification.get("operation_type"),
            classification["input"]
        )
        
        # Step 4: Select Tools
        tools = []
        if task_type:
            tools = self.tool_matrix.select_tools_for_task(task_type, context)
        else:
            # Fallback to intelligent tool selector
            tools = self.tool_selector.select_tools(user_input, max_tools=5)
        
        # Step 5: Determine Execution Strategy
        execution_strategy = self._determine_execution_strategy(
            classification,
            task_type,
            tools
        )
        
        # Step 6: Build Decision Result
        result = {
            "classification": classification,
            "parameters": params,
            "task_type": task_type,
            "selected_tools": [tool.name if hasattr(tool, 'name') else str(type(tool).__name__) for tool in tools],
            "tools": tools,  # Actual tool instances
            "execution_strategy": execution_strategy,
            "requires_confirmation": classification["confidence"] < 0.8,
            "routing": classification["routing"],
        }
        
        return result
    
    def _determine_execution_strategy(self, classification: Dict, task_type: Optional[str], tools: List[Any]) -> Dict[str, Any]:
        """Determine the execution strategy based on the decision."""
        intent = classification["intent"]
        confidence = classification["confidence"]
        operation_type = classification.get("operation_type")
        
        strategy = {
            "immediate_execution": confidence >= 0.8,
            "needs_confirmation": confidence < 0.8 and confidence >= 0.5,
            "needs_clarification": confidence < 0.5,
            "parallel_possible": False,
            "estimated_complexity": "low",
        }
        
        # Determine complexity
        if operation_type == "file_operation" and task_type in ["read_file", "create_single_file"]:
            strategy["estimated_complexity"] = "low"
        elif operation_type == "code_operation" or task_type == "generate_code":
            strategy["estimated_complexity"] = "medium"
        elif len(tools) > 3 or task_type == "complex_search":
            strategy["estimated_complexity"] = "high"
        
        # Check if parallel execution is possible
        if task_type in ["create_multiple_files", "complex_search"]:
            strategy["parallel_possible"] = True
        
        return strategy


# Global instance
_decision_engine = None

def get_decision_engine() -> DecisionEngine:
    """Get or create the global decision engine instance."""
    global _decision_engine
    if _decision_engine is None:
        _decision_engine = DecisionEngine()
    return _decision_engine

