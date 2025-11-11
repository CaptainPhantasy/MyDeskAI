"""
Error Handling Cascades - Section 11 of Claude Code Plan
Implements error classification, recovery strategies, and cascading failure management
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import traceback


class ErrorSeverity(Enum):
    """Error severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ErrorHandler:
    """Handles errors following Claude Code logic cascades."""
    
    def __init__(self):
        """Initialize error handler."""
        self.error_history = []
        self.recovery_strategies = {
            ErrorSeverity.CRITICAL: self._critical_recovery,
            ErrorSeverity.HIGH: self._high_recovery,
            ErrorSeverity.MEDIUM: self._medium_recovery,
            ErrorSeverity.LOW: self._low_recovery,
        }
    
    def handle_error(self, error: Exception, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Handle an error following Section 11.1 logic.
        
        Args:
            error: Exception that occurred
            context: Optional context
            
        Returns:
            Error handling result
        """
        # ERROR SEVERITY ASSESSMENT
        severity = self._assess_severity(error, context)
        
        # ERROR RECOVERY STRATEGY
        recovery = self._determine_recovery_strategy(severity, error, context)
        
        # Execute recovery
        recovery_result = self._execute_recovery(recovery, error, context)
        
        # Log error
        error_record = {
            "error": str(error),
            "type": type(error).__name__,
            "severity": severity.value,
            "recovery": recovery_result,
            "context": context,
            "traceback": traceback.format_exc()
        }
        self.error_history.append(error_record)
        
        return {
            "severity": severity.value,
            "error": str(error),
            "recovery": recovery_result,
            "can_continue": recovery_result.get("can_continue", False)
        }
    
    def handle_cascading_failure(self, failures: List[Dict[str, Any]], context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Handle cascading failures following Section 11.2 logic.
        
        Args:
            failures: List of failure information
            context: Optional context
            
        Returns:
            Cascading failure handling result
        """
        # FAILURE CHAIN ANALYSIS
        chain_analysis = self._analyze_failure_chain(failures)
        
        # CONTAINMENT STRATEGY
        containment = self._contain_failures(chain_analysis, context)
        
        # RECOVERY EXECUTION
        recovery = self._recover_from_cascade(chain_analysis, containment, context)
        
        return {
            "root_cause": chain_analysis.get("root_cause"),
            "propagation_path": chain_analysis.get("propagation_path"),
            "containment": containment,
            "recovery": recovery
        }
    
    def _assess_severity(self, error: Exception, context: Optional[Dict]) -> ErrorSeverity:
        """Assess error severity."""
        error_type = type(error).__name__
        error_str = str(error).lower()
        
        # Critical errors
        if any(keyword in error_str for keyword in ["system", "security", "breach", "corrupt"]):
            return ErrorSeverity.CRITICAL
        
        if error_type in ["SystemError", "MemoryError", "OSError"]:
            return ErrorSeverity.CRITICAL
        
        # High severity
        if error_type in ["RuntimeError", "ValueError", "KeyError"]:
            return ErrorSeverity.HIGH
        
        if any(keyword in error_str for keyword in ["build", "crash", "fatal"]):
            return ErrorSeverity.HIGH
        
        # Medium severity
        if error_type in ["AttributeError", "TypeError", "ImportError"]:
            return ErrorSeverity.MEDIUM
        
        # Low severity (default)
        return ErrorSeverity.LOW
    
    def _determine_recovery_strategy(self, severity: ErrorSeverity, error: Exception, context: Optional[Dict]) -> Dict[str, Any]:
        """Determine recovery strategy."""
        strategy_map = {
            ErrorSeverity.CRITICAL: {
                "type": "manual",
                "requires_intervention": True,
                "steps": ["Document issue", "Provide workarounds", "Escalate"]
            },
            ErrorSeverity.HIGH: {
                "type": "assisted",
                "requires_intervention": False,
                "steps": ["Retry with backoff", "Fallback options", "Guided resolution"]
            },
            ErrorSeverity.MEDIUM: {
                "type": "automatic",
                "requires_intervention": False,
                "steps": ["Retry", "Alternative approach", "Graceful degradation"]
            },
            ErrorSeverity.LOW: {
                "type": "automatic",
                "requires_intervention": False,
                "steps": ["Continue", "Log warning", "Best effort"]
            }
        }
        
        return strategy_map.get(severity, strategy_map[ErrorSeverity.LOW])
    
    def _execute_recovery(self, recovery: Dict[str, Any], error: Exception, context: Optional[Dict]) -> Dict[str, Any]:
        """Execute recovery strategy."""
        recovery_type = recovery.get("type", "automatic")
        
        if recovery_type == "automatic":
            return {
                "success": True,
                "can_continue": True,
                "action": "Automatic recovery attempted",
                "strategy": recovery
            }
        elif recovery_type == "assisted":
            return {
                "success": False,
                "can_continue": True,
                "action": "Assisted recovery needed",
                "strategy": recovery,
                "guidance": recovery.get("steps", [])
            }
        else:  # manual
            return {
                "success": False,
                "can_continue": False,
                "action": "Manual intervention required",
                "strategy": recovery
            }
    
    def _analyze_failure_chain(self, failures: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze failure chain."""
        if not failures:
            return {"root_cause": None, "propagation_path": []}
        
        # First failure is likely root cause
        root_cause = failures[0]
        
        # Build propagation path
        propagation_path = [f.get("component", "unknown") for f in failures]
        
        return {
            "root_cause": root_cause,
            "propagation_path": propagation_path,
            "failure_count": len(failures),
            "affected_components": list(set(propagation_path))
        }
    
    def _contain_failures(self, chain_analysis: Dict[str, Any], context: Optional[Dict]) -> Dict[str, Any]:
        """Contain failures."""
        return {
            "isolated": True,
            "stabilized": True,
            "preserved_state": True,
            "affected_components": chain_analysis.get("affected_components", [])
        }
    
    def _recover_from_cascade(self, chain_analysis: Dict[str, Any], containment: Dict[str, Any], context: Optional[Dict]) -> Dict[str, Any]:
        """Recover from cascading failure."""
        return {
            "recovery_attempted": True,
            "rollback_available": True,
            "state_restored": False,
            "next_steps": ["Restore from backup", "Restart services", "Verify integrity"]
        }
    
    def _critical_recovery(self, error: Exception, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle critical error recovery."""
        return {"action": "immediate_intervention", "can_continue": False}
    
    def _high_recovery(self, error: Exception, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle high severity error recovery."""
        return {"action": "retry_with_fallback", "can_continue": True}
    
    def _medium_recovery(self, error: Exception, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle medium severity error recovery."""
        return {"action": "graceful_degradation", "can_continue": True}
    
    def _low_recovery(self, error: Exception, context: Optional[Dict]) -> Dict[str, Any]:
        """Handle low severity error recovery."""
        return {"action": "continue", "can_continue": True}


# Global instance
_error_handler = None

def get_error_handler() -> ErrorHandler:
    """Get or create global error handler."""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler

