"""
Agent Orchestrator - Section 9 of Claude Code Plan
Handles multi-agent task decomposition and orchestration
"""

from typing import Dict, List, Any, Optional
from agents import (
    create_planner_agent,
    create_file_reader_agent,
    create_code_analyst_agent,
    create_report_writer_agent,
    create_test_agent
)
from llm_wrapper import LiteLLMWrapper
from crewai import Crew, Task
from decision_engine import get_decision_engine


class AgentOrchestrator:
    """Orchestrates multiple agents following Claude Code logic."""
    
    def __init__(self):
        """Initialize agent orchestrator."""
        self.decision_engine = get_decision_engine()
    
    def orchestrate_task(self, user_request: str, llm: LiteLLMWrapper, model_name: str = "unknown") -> Dict[str, Any]:
        """
        Orchestrate a task using multiple agents following Section 9.1 logic.
        
        Args:
            user_request: User's request
            llm: LLM wrapper
            model_name: Model name
            
        Returns:
            Orchestration result
        """
        # TASK ANALYSIS
        decision = self.decision_engine.process_request(user_request)
        complexity = decision.get("execution_strategy", {}).get("estimated_complexity", "low")
        
        # Determine if multi-agent is needed
        if complexity in ["high", "medium"] or decision.get("task_type") in ["complex_search", "analyze_code"]:
            return self._multi_agent_execution(user_request, llm, model_name, decision)
        else:
            return self._single_agent_execution(user_request, llm, model_name, decision)
    
    def _multi_agent_execution(self, request: str, llm: LiteLLMWrapper, model_name: str, decision: Dict) -> Dict[str, Any]:
        """Execute using multiple agents."""
        # AGENT ROLE ASSIGNMENT
        planner = create_planner_agent(llm, model_name)
        file_reader = create_file_reader_agent(llm, model_name, decision.get("tools", []))
        code_analyst = create_code_analyst_agent(llm, model_name, decision.get("tools", []))
        report_writer = create_report_writer_agent(llm, model_name)
        
        # Create tasks
        planning_task = Task(
            description=f"Analyze the request: {request}\n\nBreak it down into steps and coordinate other agents.",
            agent=planner,
            expected_output="A clear plan with steps for other agents"
        )
        
        execution_task = Task(
            description=f"Execute the plan for: {request}\n\nUse available tools to complete the work.",
            agent=file_reader if decision.get("task_type") == "read_file" else code_analyst,
            expected_output="Completed work based on the plan"
        )
        
        reporting_task = Task(
            description=f"Create a comprehensive report for: {request}\n\nSynthesize all information.",
            agent=report_writer,
            expected_output="A clear, comprehensive report",
            context=[planning_task, execution_task]
        )
        
        # ORCHESTRATION STRATEGY
        crew = Crew(
            agents=[planner, file_reader, code_analyst, report_writer],
            tasks=[planning_task, execution_task, reporting_task],
            verbose=True
        )
        
        return {
            "orchestration_type": "multi_agent",
            "agents": ["planner", "file_reader", "code_analyst", "report_writer"],
            "crew": crew,
            "tasks": [planning_task, execution_task, reporting_task]
        }
    
    def _single_agent_execution(self, request: str, llm: LiteLLMWrapper, model_name: str, decision: Dict) -> Dict[str, Any]:
        """Execute using single agent."""
        from agents import create_test_agent
        
        agent = create_test_agent(llm, model_name, decision.get("tools", []))
        
        task = Task(
            description=request,
            agent=agent,
            expected_output="A direct answer to the request"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        return {
            "orchestration_type": "single_agent",
            "agents": ["test_agent"],
            "crew": crew,
            "tasks": [task]
        }


# Global instance
_orchestrator = None

def get_orchestrator() -> AgentOrchestrator:
    """Get or create global orchestrator."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator

