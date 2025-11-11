# Component Map - Phase 2 Dashboard

## Streamlit Components Used

### Settings Sidebar
- `st.sidebar.title()` - Settings header
- `st.sidebar.text_input()` - API key inputs (with type="password")
- `st.sidebar.info()` - Helpful instructions
- `st.sidebar.button()` - Save/clear actions

### Chat Interface
- `st.chat_message()` - Display messages (user/assistant)
- `st.chat_input()` - User input field
- `st.empty()` - Placeholder for dynamic content
- `st.spinner()` - Loading indicator

### State Management
- `st.session_state` - Persistent state across reruns
  - `session_state.api_keys` - Dict of API keys
  - `session_state.chat_history` - List of message dicts
  - `session_state.current_model` - Selected model

### Engine Integration
- Import from Phase 1 modules:
  - `from llm_wrapper import LiteLLMWrapper`
  - `from agents import create_test_agent`
  - `from tasks import create_test_task`
  - `from crewai import Crew`

### Error Handling
- `st.error()` - Error messages
- `st.warning()` - Warnings
- `st.success()` - Success feedback
- `st.info()` - Informational messages

### Layout
- `st.title()` - Main page title
- `st.header()` - Section headers
- `st.markdown()` - Rich text content
- `st.columns()` - Multi-column layout (if needed)

