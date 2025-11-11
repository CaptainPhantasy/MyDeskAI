# Crew Deployment Syntax Guide for MyDeskAI

Complete syntax reference for deploying crews of agents on tasks in MyDeskAI.

## Basic Syntax

### 1. Single Agent Crew (Simplest)

```python
from crewai import Crew, Task
from agents import create_test_agent
from tasks import create_test_task
from llm_wrapper import LiteLLMWrapper

# Create LLM wrapper
# Note: API keys should be set in environment variables (GEMINI_API_KEY or OPENAI_API_KEY)
llm = LiteLLMWrapper(model_name="gpt-3.5-turbo", temperature=0.7)

# Create agent
agent = create_test_agent(llm, model_name="gpt-3.5-turbo")

# Create task
task = create_test_task(agent, user_prompt="Your task here")

# Create crew
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

# Deploy the crew
result = crew.kickoff()
print(result)
```

### 2. Multi-Agent Crew (Recommended for Complex Tasks)

```python
from crewai import Crew, Task
from agents import (
    create_planner_agent,
    create_file_reader_agent,
    create_code_analyst_agent,
    create_report_writer_agent
)
from llm_wrapper import LiteLLMWrapper

# Create LLM wrapper
# Note: API keys should be set in environment variables (GEMINI_API_KEY or OPENAI_API_KEY)
llm = LiteLLMWrapper(model_name="gpt-3.5-turbo", temperature=0.7)

# Create multiple agents
planner = create_planner_agent(llm, model_name="gpt-3.5-turbo")
file_reader = create_file_reader_agent(llm, model_name="gpt-3.5-turbo")
code_analyst = create_code_analyst_agent(llm, model_name="gpt-3.5-turbo")
report_writer = create_report_writer_agent(llm, model_name="gpt-3.5-turbo")

# Create tasks with dependencies
planning_task = Task(
    description="Analyze the request and create a plan",
    agent=planner,
    expected_output="A clear plan with steps"
)

execution_task = Task(
    description="Execute the plan using available tools",
    agent=file_reader,  # or code_analyst depending on task
    expected_output="Completed work based on the plan",
    context=[planning_task]  # This task depends on planning_task
)

reporting_task = Task(
    description="Create a comprehensive report",
    agent=report_writer,
    expected_output="A clear, comprehensive report",
    context=[planning_task, execution_task]  # Depends on both previous tasks
)

# Create crew with all agents and tasks
crew = Crew(
    agents=[planner, file_reader, code_analyst, report_writer],
    tasks=[planning_task, execution_task, reporting_task],
    verbose=True,
    process=Process.sequential  # Tasks execute in order
)

# Deploy the crew
result = crew.kickoff()
print(result)
```

## Crew Parameters

### Required Parameters

- **`agents`**: List of Agent objects
  ```python
  agents=[agent1, agent2, agent3]
  ```

- **`tasks`**: List of Task objects
  ```python
  tasks=[task1, task2, task3]
  ```

### Optional Parameters

- **`process`**: Execution flow
  ```python
  process=Process.sequential  # Tasks run one after another (default)
  process=Process.hierarchical  # Manager agent coordinates
  ```

- **`verbose`**: Logging level
  ```python
  verbose=True  # Detailed logs
  verbose=False  # Minimal logs (default)
  ```

- **`manager_llm`**: LLM for hierarchical process
  ```python
  manager_llm=llm_wrapper  # Required for hierarchical
  ```

- **`max_rpm`**: Rate limiting
  ```python
  max_rpm=60  # Max 60 requests per minute
  ```

- **`memory`**: Memory for agents
  ```python
  from crewai import Memory
  memory=Memory()
  ```

- **`cache`**: Tool result caching
  ```python
  cache=True  # Cache tool results (default)
  cache=False  # Don't cache
  ```

## Task Dependencies (Context)

Tasks can depend on other tasks using the `context` parameter:

```python
task1 = Task(
    description="First task",
    agent=agent1,
    expected_output="Output from task 1"
)

task2 = Task(
    description="Second task that uses task1's output",
    agent=agent2,
    expected_output="Output from task 2",
    context=[task1]  # task2 receives task1's output
)

task3 = Task(
    description="Final task using both previous tasks",
    agent=agent3,
    expected_output="Final output",
    context=[task1, task2]  # Receives outputs from both
)
```

## Complete Example: Code Review Crew

```python
from crewai import Crew, Task, Process
from agents import (
    create_file_reader_agent,
    create_code_analyst_agent,
    create_report_writer_agent
)
from llm_wrapper import LiteLLMWrapper

# Setup
# Note: API keys should be set in environment variables (GEMINI_API_KEY or OPENAI_API_KEY)
llm = LiteLLMWrapper(model_name="gpt-3.5-turbo", temperature=0.7)
file_path = "app.py"

# Create agents
file_reader = create_file_reader_agent(llm, model_name="gpt-3.5-turbo")
code_analyst = create_code_analyst_agent(llm, model_name="gpt-3.5-turbo")
report_writer = create_report_writer_agent(llm, model_name="gpt-3.5-turbo")

# Create tasks
read_task = Task(
    description=f"Read and analyze the file: {file_path}",
    agent=file_reader,
    expected_output="Complete file content and structure analysis"
)

analysis_task = Task(
    description="Analyze the code for quality, bugs, and improvements",
    agent=code_analyst,
    expected_output="Detailed code analysis with findings",
    context=[read_task]  # Uses read_task output
)

report_task = Task(
    description="Create a comprehensive code review report",
    agent=report_writer,
    expected_output="Professional code review report",
    context=[read_task, analysis_task]  # Uses both previous outputs
)

# Create crew
crew = Crew(
    agents=[file_reader, code_analyst, report_writer],
    tasks=[read_task, analysis_task, report_task],
    process=Process.sequential,  # Execute in order
    verbose=True
)

# Deploy
result = crew.kickoff()
print(result)
```

## Using the Orchestrator (Automatic)

MyDeskAI includes an orchestrator that automatically creates crews:

```python
from agent_orchestrator import get_orchestrator
from llm_wrapper import LiteLLMWrapper

# Note: API keys should be set in environment variables (GEMINI_API_KEY or OPENAI_API_KEY)
llm = LiteLLMWrapper(model_name="gpt-3.5-turbo", temperature=0.7)
orchestrator = get_orchestrator()

# Automatically creates appropriate crew based on request complexity
orchestration = orchestrator.orchestrate_task(
    user_request="Review the code in app.py",
    llm=llm,
    model_name="gpt-3.5-turbo"
)

# Get the crew
crew = orchestration["crew"]

# Deploy
result = crew.kickoff()
```

## Crew Execution Methods

### Synchronous Execution
```python
result = crew.kickoff()
result = crew.kickoff(inputs={"key": "value"})  # With inputs
```

### Asynchronous Execution
```python
result = await crew.kickoff_async()
result = await crew.kickoff_async(inputs={"key": "value"})
```

### Batch Execution
```python
# Execute crew for multiple inputs
results = crew.kickoff_for_each(
    inputs=[
        {"file": "app.py"},
        {"file": "utils.py"},
        {"file": "test.py"}
    ]
)
```

## Accessing Results

```python
result = crew.kickoff()

# Different ways to access output
if hasattr(result, 'raw'):
    output = result.raw
elif hasattr(result, 'output'):
    output = result.output
else:
    output = str(result)

# Access individual task outputs
for task in crew.tasks:
    print(f"Task: {task.description}")
    print(f"Output: {task.output}")
```

## Common Patterns

### Pattern 1: Sequential Pipeline
```python
crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True
)
```

### Pattern 2: Parallel Execution
```python
# Tasks without dependencies can run in parallel
task1 = Task(..., agent=agent1)
task2 = Task(..., agent=agent2)  # No context dependency
task3 = Task(..., agent=agent3, context=[task1, task2])  # Waits for both

crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    verbose=True
)
```

### Pattern 3: Hierarchical (Manager Coordinates)
```python
from crewai import Process

crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_llm=llm_wrapper,  # Required for hierarchical
    verbose=True
)
```

## Best Practices

1. **Always assign tasks to agents**: Each task must have an `agent` parameter
2. **Use context for dependencies**: Tasks that need previous outputs should use `context=[previous_task]`
3. **Set expected_output**: Helps agents understand what's needed
4. **Use verbose=True**: For debugging and monitoring
5. **Match agents to tasks**: Assign tasks to agents with appropriate tools/expertise
6. **Handle results properly**: Check for `result.raw`, `result.output`, or `str(result)`

## Quick Reference

```python
# Minimal crew
crew = Crew(agents=[agent], tasks=[task], verbose=True)
result = crew.kickoff()

# Full crew with all options
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True,
    max_rpm=60,
    memory=Memory(),
    cache=True
)
result = crew.kickoff(inputs={"key": "value"})
```

