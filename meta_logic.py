"""
Meta-Logic & Continuous Improvement - Section 12 of Claude Code Plan
Implements task prioritization, learning, and self-evaluation
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict


class MetaLogic:
    """Implements meta-logic for continuous improvement."""
    
    def __init__(self):
        """Initialize meta-logic system."""
        self.task_history = []
        self.pattern_recognition = defaultdict(int)
        self.user_preferences = {}
        self.error_patterns = defaultdict(int)
        self.performance_metrics = []
    
    def prioritize_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritize tasks following Section 12.1 logic.
        
        Args:
            tasks: List of tasks to prioritize
            
        Returns:
            Prioritized task list
        """
        # PRIORITY ASSESSMENT
        for task in tasks:
            priority_score = self._calculate_priority(task)
            task["priority_score"] = priority_score
        
        # Sort by priority
        sorted_tasks = sorted(tasks, key=lambda x: x["priority_score"], reverse=True)
        
        # EXECUTION PLANNING
        execution_plan = self._plan_execution(sorted_tasks)
        
        return execution_plan
    
    def learn_from_interaction(self, interaction: Dict[str, Any]) -> None:
        """
        Learn from interactions following Section 12.2 logic.
        
        Args:
            interaction: Interaction data to learn from
        """
        # Pattern Recognition
        task_type = interaction.get("task_type")
        if task_type:
            self.pattern_recognition[task_type] += 1
        
        # Error Patterns
        if "error" in interaction:
            error_type = interaction["error"].get("type")
            if error_type:
                self.error_patterns[error_type] += 1
        
        # User Preferences
        if "user_feedback" in interaction:
            feedback = interaction["user_feedback"]
            if "preferred_format" in feedback:
                self.user_preferences["output_format"] = feedback["preferred_format"]
            if "preferred_style" in feedback:
                self.user_preferences["code_style"] = feedback["preferred_style"]
        
        # Performance Metrics
        if "execution_time" in interaction:
            self.performance_metrics.append({
                "time": interaction["execution_time"],
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            })
    
    def self_evaluate(self, task_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Self-evaluate task completion following Section 12.2 checkpoints.
        
        Args:
            task_result: Result of completed task
            
        Returns:
            Self-evaluation results
        """
        evaluation = {
            "completed_fully": task_result.get("success", False),
            "unnecessary_steps": self._check_unnecessary_steps(task_result),
            "conciseness": self._evaluate_conciseness(task_result),
            "conventions_followed": self._check_conventions(task_result),
            "edge_cases_considered": self._check_edge_cases(task_result),
            "maintainable": self._check_maintainability(task_result),
            "clear_communication": self._check_communication(task_result)
        }
        
        # Overall score
        evaluation["overall_score"] = sum([
            1 if evaluation["completed_fully"] else 0,
            1 if not evaluation["unnecessary_steps"] else 0,
            1 if evaluation["conciseness"] > 0.7 else 0,
            1 if evaluation["conventions_followed"] else 0,
            1 if evaluation["edge_cases_considered"] else 0,
            1 if evaluation["maintainable"] else 0,
            1 if evaluation["clear_communication"] else 0
        ]) / 7.0
        
        return evaluation
    
    def _calculate_priority(self, task: Dict[str, Any]) -> float:
        """Calculate priority score for a task."""
        score = 0.5  # Base score
        
        # Blocking issues
        if task.get("blocking", False):
            score += 0.3
        
        # Dependencies
        if task.get("has_dependencies", False):
            score += 0.2
        
        # User emphasis
        if any(word in str(task.get("description", "")).lower() for word in ["urgent", "asap", "critical"]):
            score += 0.2
        
        # Efficiency (group similar tasks)
        task_type = task.get("type")
        if task_type in self.pattern_recognition:
            score += 0.1  # Slight boost for known patterns
        
        return min(1.0, score)
    
    def _plan_execution(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Plan task execution."""
        execution_plan = []
        
        for task in tasks:
            # Check if parallel execution is possible
            can_parallel = not task.get("has_dependencies", False)
            
            execution_plan.append({
                **task,
                "can_parallel": can_parallel,
                "estimated_time": self._estimate_time(task),
                "risk_level": self._assess_risk(task)
            })
        
        return execution_plan
    
    def _estimate_time(self, task: Dict[str, Any]) -> str:
        """Estimate task execution time."""
        task_type = task.get("type", "unknown")
        
        time_estimates = {
            "file_operation": "quick",
            "code_generation": "medium",
            "test_execution": "medium",
            "complex_analysis": "long"
        }
        
        return time_estimates.get(task_type, "medium")
    
    def _assess_risk(self, task: Dict[str, Any]) -> str:
        """Assess task risk level."""
        if task.get("destructive", False):
            return "high"
        elif task.get("has_dependencies", False):
            return "medium"
        else:
            return "low"
    
    def _check_unnecessary_steps(self, task_result: Dict[str, Any]) -> bool:
        """Check if unnecessary steps were taken."""
        steps = task_result.get("steps_taken", [])
        return len(steps) <= 3  # Reasonable number of steps
    
    def _evaluate_conciseness(self, task_result: Dict[str, Any]) -> float:
        """Evaluate response conciseness."""
        output = str(task_result.get("output", ""))
        # Shorter is better, but not too short
        length = len(output)
        if length < 100:
            return 0.5  # Too short
        elif length < 1000:
            return 1.0  # Good length
        elif length < 5000:
            return 0.8  # Acceptable
        else:
            return 0.5  # Too long
    
    def _check_conventions(self, task_result: Dict[str, Any]) -> bool:
        """Check if project conventions were followed."""
        # This would check against project-specific conventions
        return True  # Placeholder
    
    def _check_edge_cases(self, task_result: Dict[str, Any]) -> bool:
        """Check if edge cases were considered."""
        return task_result.get("edge_cases_handled", False)
    
    def _check_maintainability(self, task_result: Dict[str, Any]) -> bool:
        """Check if solution is maintainable."""
        output = str(task_result.get("output", ""))
        # Check for good practices
        has_comments = "#" in output or "//" in output
        has_docstrings = '"""' in output or "'''" in output
        return has_comments or has_docstrings
    
    def _check_communication(self, task_result: Dict[str, Any]) -> bool:
        """Check if communication was clear."""
        return task_result.get("explanation_provided", True)


# Global instance
_meta_logic = None

def get_meta_logic() -> MetaLogic:
    """Get or create global meta-logic instance."""
    global _meta_logic
    if _meta_logic is None:
        _meta_logic = MetaLogic()
    return _meta_logic

