"""
My Desk AI - Streamlit Dashboard
Phase 2: MVP Dashboard Implementation

This module provides the Streamlit UI for interacting with AI agent swarms.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew
from llm_wrapper import LiteLLMWrapper
from agents import (
    create_test_agent,
    create_planner_agent,
    create_file_reader_agent,
    create_code_analyst_agent,
    create_report_writer_agent
)
from tasks import create_test_task
from smart_router import route_model
from tool_selector import get_tool_selector
from decision_engine import get_decision_engine
from agent_orchestrator import get_orchestrator
from error_handling_cascades import get_error_handler
from output_formatter import get_output_formatter
from crewai.events.event_bus import crewai_event_bus
from crewai.events.base_event_listener import BaseEventListener
from crewai.events.types.llm_events import LLMStreamChunkEvent
from crewai.events.types.agent_events import (
    AgentExecutionStartedEvent,
    AgentExecutionCompletedEvent,
    AgentExecutionErrorEvent
)
from crewai.events.types.task_events import (
    TaskStartedEvent,
    TaskCompletedEvent,
    TaskFailedEvent
)
from crewai.events.types.tool_usage_events import (
    ToolUsageStartedEvent,
    ToolUsageFinishedEvent,
    ToolUsageErrorEvent
)


def load_keys_from_env():
    """Load API keys from .env file if it exists."""
    load_dotenv()
    keys = {
        "gemini": os.getenv("GEMINI_API_KEY", "").strip('"').strip("'"),
        "openai": os.getenv("OPENAI_API_KEY", "").strip('"').strip("'"),
        "glm": os.getenv("GLM_API_KEY", "").strip('"').strip("'"),
    }
    return keys


# Initialize session state
if "api_keys" not in st.session_state:
    # Try to load from .env file first
    env_keys = load_keys_from_env()
    st.session_state.api_keys = {
        "gemini": env_keys.get("gemini", ""),
        "openai": env_keys.get("openai", ""),
        "glm": env_keys.get("glm", ""),
    }

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_model" not in st.session_state:
    st.session_state.current_model = "gpt-3.5-turbo"


class StreamlitStreamListener(BaseEventListener):
    """Event listener to capture streaming chunks and agent activity for Streamlit display."""
    
    def __init__(self, stream_container, log_container=None):
        self.stream_container = stream_container
        self.log_container = log_container
        self.accumulated_text = ""
        self.activity_log = []  # Store activity log entries
        self.setup_listeners()
    
    def setup_listeners(self):
        # Existing listener for final text output
        @crewai_event_bus.on(LLMStreamChunkEvent)
        def on_llm_stream_chunk(event: LLMStreamChunkEvent):
            """Handle each streaming chunk."""
            if event.chunk:
                self.accumulated_text += event.chunk
                # Update the stream container with accumulated text
                self.stream_container.markdown(self.accumulated_text)
        
        # Agent execution events
        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def on_agent_started(event: AgentExecutionStartedEvent):
            """Handle when an agent starts executing."""
            agent_name = getattr(event.agent, 'role', 'Unknown Agent')
            message = f"🤖 **{agent_name}** started working on task"
            self._add_log_entry(message, "info")
        
        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_completed(event: AgentExecutionCompletedEvent):
            """Handle when an agent completes execution."""
            agent_name = getattr(event.agent, 'role', 'Unknown Agent')
            output_preview = str(event.output)[:150] + "..." if len(str(event.output)) > 150 else str(event.output)
            message = f"✅ **{agent_name}** completed task\n\n*Output preview: {output_preview}*"
            self._add_log_entry(message, "success")
        
        @crewai_event_bus.on(AgentExecutionErrorEvent)
        def on_agent_error(event: AgentExecutionErrorEvent):
            """Handle when an agent encounters an error."""
            agent_name = getattr(event.agent, 'role', 'Unknown Agent')
            message = f"❌ **{agent_name}** encountered an error: {event.error}"
            self._add_log_entry(message, "error")
        
        # Task events
        @crewai_event_bus.on(TaskStartedEvent)
        def on_task_started(event: TaskStartedEvent):
            """Handle when a task starts."""
            task_name = getattr(event.task, 'description', 'Unknown Task')[:100] if event.task else "Unknown Task"
            message = f"📋 Task started: *{task_name}*"
            self._add_log_entry(message, "info")
        
        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(event: TaskCompletedEvent):
            """Handle when a task completes."""
            task_name = getattr(event.task, 'description', 'Unknown Task')[:100] if event.task else "Unknown Task"
            output_preview = str(event.output)[:150] + "..." if len(str(event.output)) > 150 else str(event.output)
            message = f"✅ Task completed: *{task_name}*\n\n*Output: {output_preview}*"
            self._add_log_entry(message, "success")
        
        @crewai_event_bus.on(TaskFailedEvent)
        def on_task_failed(event: TaskFailedEvent):
            """Handle when a task fails."""
            task_name = getattr(event.task, 'description', 'Unknown Task')[:100] if event.task else "Unknown Task"
            message = f"❌ Task failed: *{task_name}*\n\n*Error: {event.error}*"
            self._add_log_entry(message, "error")
        
        # Tool usage events
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_started(event: ToolUsageStartedEvent):
            """Handle when a tool execution starts."""
            agent_role = event.agent_role or "Unknown Agent"
            tool_name = event.tool_name
            tool_args = str(event.tool_args)[:100] if event.tool_args else "No args"
            message = f"🔧 **{agent_role}** using tool: `{tool_name}`\n*Input: {tool_args}*"
            self._add_log_entry(message, "info")
        
        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_finished(event: ToolUsageFinishedEvent):
            """Handle when a tool execution completes."""
            agent_role = event.agent_role or "Unknown Agent"
            tool_name = event.tool_name
            output_preview = str(event.output)[:150] + "..." if len(str(event.output)) > 150 else str(event.output)
            cache_status = " (cached)" if event.from_cache else ""
            message = f"✅ **{agent_role}** finished using `{tool_name}`{cache_status}\n*Output: {output_preview}*"
            self._add_log_entry(message, "success")
        
        @crewai_event_bus.on(ToolUsageErrorEvent)
        def on_tool_error(event: ToolUsageErrorEvent):
            """Handle when a tool execution encounters an error."""
            agent_role = event.agent_role or "Unknown Agent"
            tool_name = event.tool_name
            error_msg = str(event.error)[:200]
            message = f"❌ **{agent_role}** error with tool `{tool_name}`: {error_msg}"
            self._add_log_entry(message, "error")
    
    def _add_log_entry(self, message: str, level: str = "info"):
        """Add an entry to the activity log and update the UI."""
        self.activity_log.append({"message": message, "level": level})
        
        # Update the log container if available
        if self.log_container:
            # Clear and rebuild the log display
            log_text = ""
            for entry in self.activity_log[-20:]:  # Show last 20 entries
                if entry["level"] == "info":
                    log_text += f"ℹ️ {entry['message']}\n\n"
                elif entry["level"] == "success":
                    log_text += f"✅ {entry['message']}\n\n"
                elif entry["level"] == "error":
                    log_text += f"❌ {entry['message']}\n\n"
                else:
                    log_text += f"{entry['message']}\n\n"
            
            self.log_container.markdown(log_text)


def render_settings_sidebar():
    """Render the settings sidebar for API key management."""
    with st.sidebar:
        st.title("Settings")
        
        st.markdown("### API Keys")
        
        # Check if .env file exists and offer to load from it
        env_file_exists = os.path.exists(".env")
        if env_file_exists and not st.session_state.api_keys.get("openai") and not st.session_state.api_keys.get("gemini"):
            if st.button("Load Keys from .env File", use_container_width=True):
                env_keys = load_keys_from_env()
                st.session_state.api_keys["gemini"] = env_keys.get("gemini", "")
                st.session_state.api_keys["openai"] = env_keys.get("openai", "")
                st.rerun()
            st.info("Found .env file. Click above to load keys, or enter manually below.")
        elif env_file_exists:
            st.success("Keys loaded from .env file")
        else:
            st.info("Enter your API keys below. Keys are stored securely in session state.")
        
        # Gemini API Key
        gemini_key = st.text_input(
            "Google Gemini API Key",
            value=st.session_state.api_keys["gemini"],
            type="password",
            help="Get your key from https://aistudio.google.com/app/apikey",
            key="gemini_key_input"
        )
        
        # OpenAI API Key
        openai_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_keys["openai"],
            type="password",
            help="Get your key from https://platform.openai.com/api-keys",
            key="openai_key_input"
        )
        
        # GLM-4.6 API Key (Zhipu AI)
        glm_key = st.text_input(
            "GLM-4.6 API Key (Zhipu AI)",
            value=st.session_state.api_keys["glm"],
            type="password",
            help="Get your key from https://open.bigmodel.cn/",
            key="glm_key_input"
        )
        
        # Save keys to session state
        if gemini_key != st.session_state.api_keys["gemini"]:
            st.session_state.api_keys["gemini"] = gemini_key
            st.rerun()
        
        if openai_key != st.session_state.api_keys["openai"]:
            st.session_state.api_keys["openai"] = openai_key
            st.rerun()
        
        if glm_key != st.session_state.api_keys["glm"]:
            st.session_state.api_keys["glm"] = glm_key
            st.rerun()
        
        # Model selection
        st.markdown("### Model Selection")
        available_models = []
        # Prioritize GLM-4.6 (user's preferred model)
        if st.session_state.api_keys["glm"]:
            available_models.append("glm-4.6")
        # OpenAI as fallback
        if st.session_state.api_keys["openai"]:
            available_models.append("gpt-3.5-turbo")
        # Note: Gemini support is experimental - crewai tries to use native provider
        # if st.session_state.api_keys["gemini"]:
        #     available_models.append("gemini/gemini-1.5-flash")
        
        if available_models:
            # Default to OpenAI if available, otherwise first available
            default_index = 0
            if st.session_state.current_model not in available_models:
                st.session_state.current_model = available_models[0]
            else:
                default_index = available_models.index(st.session_state.current_model)
            
            selected_model = st.selectbox(
                "Select Model",
                options=available_models,
                index=default_index,
                help="Choose which LLM to use for agent responses."
            )
            st.session_state.current_model = selected_model
        else:
            st.warning("Please add at least one API key to continue.")
            st.session_state.current_model = None
        
        # Info about Gemini
        if st.session_state.api_keys["gemini"] and not st.session_state.api_keys["openai"] and not st.session_state.api_keys["glm"]:
            st.info("Gemini key detected but Gemini support is currently disabled due to crewai compatibility. Please add a GLM-4.6 or OpenAI key for full functionality.")
        
        # Clear chat button
        st.markdown("---")
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        # Status indicator
        st.markdown("---")
        st.markdown("### Status")
        if st.session_state.api_keys["glm"] or st.session_state.api_keys["openai"] or st.session_state.api_keys["gemini"]:
            st.success("Ready")
            if st.session_state.api_keys["glm"]:
                st.info("GLM-4.6 is configured and will be used as default")
        else:
            st.error("No API keys configured")


def render_chat_interface():
    """Render the main chat interface."""
    st.title("My Desk AI")
    st.markdown("Chat with your AI agent swarm. Enter a task below and watch the agents work.")
    
    # Display chat history or empty state
    if not st.session_state.chat_history:
        # Empty state
        st.markdown("---")
        with st.container():
            st.markdown("### Get Started")
            st.markdown("""
            **Simple Questions**: Ask anything and get a direct answer.
            
            **File Analysis**: Ask to read or analyze files (e.g., "Read app.py and analyze the code").
            
            **Code Review**: Request code analysis (e.g., "Review the agents.py file for best practices").
            
            **Complex Tasks**: The agent swarm will automatically coordinate multiple agents for complex requests.
            """)
        st.markdown("---")
    else:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Enter your task or question..."):
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Check if API keys are configured
        if not st.session_state.current_model:
            with st.chat_message("assistant"):
                st.error("Please configure at least one API key in the Settings sidebar to continue.")
            return
        
        # Process the request
        process_user_request(prompt)


def process_user_request(prompt: str):
    """Process a user request by creating and running a crew."""
    with st.chat_message("assistant"):
        # Set up API keys in environment
        if st.session_state.api_keys["gemini"]:
            os.environ["GEMINI_API_KEY"] = st.session_state.api_keys["gemini"]
        if st.session_state.api_keys["openai"]:
            os.environ["OPENAI_API_KEY"] = st.session_state.api_keys["openai"]
        if st.session_state.api_keys["glm"]:
            os.environ["ZHIPUAI_API_KEY"] = st.session_state.api_keys["glm"]
        
        # Create activity log container (expander for agent work visibility)
        log_expander = st.expander("🔍 Agent Activity Log", expanded=True)
        with log_expander:
            log_container = st.empty()
            log_container.info("Waiting for agent activity...")
        
        # Create stream container for real-time output
        stream_placeholder = st.empty()
        
        try:
            with st.spinner("Processing your request..."):
                # Validate model selection
                if not st.session_state.current_model:
                    raise ValueError("No model selected. Please configure API keys and select a model.")
                
                # Smart router: select best model based on prompt (prioritize GLM-4.6)
                available_models = []
                if st.session_state.api_keys["glm"]:
                    available_models.append("glm-4.6")
                if st.session_state.api_keys["openai"]:
                    available_models.append("gpt-3.5-turbo")
                
                model_name = route_model(prompt, available_models)
                
                # Create LLM wrapper with GLM-4.6 configuration if needed
                api_base = None
                api_key = None
                
                if model_name == "glm-4.6":
                    # GLM-4.6 API Configuration (per official docs: https://apidog.com/blog/glm-4-6-api/)
                    # Endpoint: https://api.z.ai/api/paas/v4/chat/completions
                    # Model: "glm-4.6"
                    # Authentication: Bearer token
                    api_base = "https://api.z.ai/api/paas/v4"  # LiteLLM appends /chat/completions
                    api_key = st.session_state.api_keys.get("glm")
                    model_name = "glm-4.6"  # Official model name
                
                llm = LiteLLMWrapper(
                    model_name=model_name,
                    temperature=0.7,
                    api_base=api_base,
                    api_key=api_key,
                )
                
                # Use Claude Code decision engine and orchestrator
                decision_engine = get_decision_engine()
                orchestrator = get_orchestrator()
                error_handler = get_error_handler()
                
                context = {
                    "current_directory": os.getcwd(),
                    "project_type": "python",
                }
                
                decision = None
                try:
                    # Process request through decision engine
                    decision = decision_engine.process_request(prompt, context=context)
                    
                    # Orchestrate using appropriate agent strategy
                    orchestration = orchestrator.orchestrate_task(prompt, llm, model_name)
                    
                    # Use orchestrated crew
                    crew = orchestration["crew"]
                    
                except Exception as e:
                    # Error handling cascade
                    error_result = error_handler.handle_error(e, context={"prompt": prompt})
                    
                    if error_result.get("can_continue"):
                        # Fallback to simple agent
                        selected_tools = decision.get("tools", []) if decision else []
                        agent = create_test_agent(llm, model_name=model_name, tools=selected_tools)
                        task = create_test_task(agent, prompt)
                        crew = Crew(agents=[agent], tasks=[task], verbose=True)
                    else:
                        raise
                
                # Set up streaming listener with log container
                # Note: We keep a reference to the listener to ensure event handlers remain active
                _listener = StreamlitStreamListener(stream_placeholder, log_container)
                
                # Run the crew
                result = crew.kickoff()
                
                # Get final result text - crewai returns the task output
                if hasattr(result, 'raw'):
                    final_text = str(result.raw) if result.raw else str(result)
                elif hasattr(result, 'output'):
                    final_text = str(result.output) if result.output else str(result)
                else:
                    final_text = str(result)
                
                # Clean up the response - remove any generic prefixes
                if final_text.startswith("I am an AI assistant") or final_text.startswith("I'm an AI assistant"):
                    # Try to extract the actual answer part
                    final_text = final_text.split(".", 1)[1].strip() if "." in final_text else final_text
                
                # Update stream container with final result
                stream_placeholder.markdown(final_text)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": final_text
                })
                
        except Exception as e:
            error_message = f"Error: {str(e)}"
            stream_placeholder.error(error_message)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_message
            })


def main():
    """Main application entry point."""
    # Configure page
    st.set_page_config(
        page_title="My Desk AI",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Render UI components
    render_settings_sidebar()
    render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
        "Built with Streamlit, CrewAI, and LiteLLM"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

