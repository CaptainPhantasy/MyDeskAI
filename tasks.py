"""
Task Definitions - Task 1.4 & Phase 3
This module defines the tasks that agents will perform.
"""

from crewai import Task


def create_test_task(agent, user_prompt: str = "Tell me a joke.") -> Task:
    """
    Create a simple test task for Phase 1 validation.
    
    Args:
        agent: The agent that will perform this task
        user_prompt: The prompt/question for the agent
        
    Returns:
        A configured Task instance
    """
    # Check if prompt mentions files
    prompt_lower = user_prompt.lower()
    mentions_file = any(keyword in prompt_lower for keyword in ["read", "file", "analyze", "code", "review", ".py", ".md", ".txt"])
    
    if mentions_file and hasattr(agent, 'tools') and agent.tools:
        # Task for file reading - explicitly instruct to use FileReadTool
        return Task(
            description=f"""The user has asked: "{user_prompt}"

IMPORTANT: The user is asking about a file. You MUST use the FileReadTool to read the file first.

HOW TO USE FileReadTool:
- Call FileReadTool with file_path parameter
- Example: FileReadTool(file_path="app.py") to read app.py
- The tool will return the file content - use that content to answer

Steps:
1. Identify the file path from the user's request (e.g., "app.py" → file_path="app.py")
2. IMMEDIATELY call FileReadTool(file_path="the_file_path") 
3. Wait for the tool to return the file content
4. Read and analyze the ENTIRE file content returned by the tool
5. Answer the user's question based on the ACTUAL file content you just read
6. If asked what model you are, identify yourself clearly

DO NOT say you cannot read files - you have FileReadTool available. CALL IT NOW with the file path!""",
            agent=agent,
            expected_output="A direct answer based on the file content you read using FileReadTool",
        )
    else:
        # Regular task - for a powerful coding assistant
        return Task(
            description=f"""The user has asked: "{user_prompt}"

You are a senior software engineer. Approach this with deep technical understanding:

**YOUR APPROACH:**
1. **Understand the Request**: Parse what they're really asking - is it code generation, analysis, debugging, or explanation?
2. **Gather Context**: If this involves code/files, IMMEDIATELY use FileReadTool to read relevant files
3. **Apply Expertise**: Use your deep knowledge of programming, architecture, and best practices
4. **Provide Solutions**: Give concrete, actionable answers - code examples, specific fixes, architectural insights
5. **Be Technical**: Use proper terminology, show code, explain trade-offs

**RESPONSE REQUIREMENTS:**
- Direct and technical - no fluff or generic assistant language
- Actionable - provide code, solutions, or specific guidance
- Precise - use exact terms, file paths, function names
- Professional - like a senior engineer would respond
- If asked what model you are: "I am [model_name], a senior software engineer AI assistant"

**DO NOT:**
- Give generic "I'm here to help" responses
- Say you cannot do something without trying tools first
- Provide vague answers - be specific and technical
- Use assistant-like language - be a coding expert

Solve the problem. Provide the solution. Be a senior engineer.""",
            agent=agent,
            expected_output="A technical, specific, actionable response that solves the user's problem or answers their question with deep coding expertise",
        )


def create_planning_task(planner_agent, user_prompt: str) -> Task:
    """Create a planning task for the Planner agent."""
    return Task(
        description=f"""Analyze the user's request: "{user_prompt}"

Break down this request into clear, actionable steps. Identify:
1. What files need to be read (if any)
2. What analysis needs to be performed
3. What output format is needed
4. The sequence of work for other agents

Create a clear plan that coordinates the work of FileReader, CodeAnalyst, and ReportWriter agents.""",
        agent=planner_agent,
        expected_output="A clear, structured plan breaking down the user's request into actionable steps",
    )


def create_file_reading_task(file_reader_agent, file_path: str) -> Task:
    """Create a file reading task."""
    return Task(
        description=f"""Read and analyze the file: {file_path}

Extract key information including:
- File structure and organization
- Key functions, classes, or sections
- Important data or configuration
- Any notable patterns or issues

Present this information clearly for other agents to use.""",
        agent=file_reader_agent,
        expected_output="A clear summary of the file's contents, structure, and key information",
    )


def create_code_analysis_task(code_analyst_agent, code_context: str, requirements: str = "") -> Task:
    """Create a code analysis task."""
    return Task(
        description=f"""Analyze the provided code.

Context: {code_context}
Requirements: {requirements if requirements else "General code quality and best practices"}

Evaluate:
- Code quality and correctness
- Adherence to requirements (if provided)
- Potential bugs or issues
- Best practices and improvements
- Code organization and structure""",
        agent=code_analyst_agent,
        expected_output="A comprehensive code analysis report with findings and recommendations",
    )


def create_report_writing_task(report_writer_agent, analysis_data: str, user_request: str) -> Task:
    """Create a report writing task."""
    return Task(
        description=f"""Create a comprehensive report based on the analysis.

User's original request: {user_request}
Analysis data from other agents: {analysis_data}

Synthesize all the information into a clear, well-structured report that:
- Directly addresses the user's request
- Presents findings clearly
- Provides actionable insights
- Is easy to understand""",
        agent=report_writer_agent,
        expected_output="A clear, comprehensive report that addresses the user's request",
    )

