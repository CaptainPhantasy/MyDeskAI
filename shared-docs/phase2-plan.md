# Phase 2: MVP Dashboard - Swarm Plan

## Overview
Build the Streamlit dashboard that provides a clean, user-centric interface for managing AI agent swarms.

## Design Principles (Adapted for Streamlit)
1. **Simplicity**: Clean, uncluttered interface that gets out of the way
2. **State Management**: Use `st.session_state` exclusively (no .env file in UI)
3. **Feedback**: Loading states, error states, empty states for all interactions
4. **Accessibility**: Clear labels, keyboard navigation support, proper form semantics
5. **User Experience**: Smooth interactions, clear visual hierarchy, helpful messaging

## Task Dependencies

```
T001: Main App Structure (app.py)
  └─ No dependencies

T002: Settings Sidebar
  └─ Depends on: T001

T003: Chat Interface UI
  └─ Depends on: T001

T004: State Management Layer
  └─ Depends on: T002, T003

T005: Engine Integration
  └─ Depends on: T004

T006: Streaming Output Handler
  └─ Depends on: T005

T007: Error Handling & Validation
  └─ Depends on: T005, T006

T008: Loading States & Feedback
  └─ Depends on: T005, T006, T007
```

## Wave Structure

### Wave 1: Foundation (T001, T002, T004)
- Create app.py with proper structure
- Implement settings sidebar with API key inputs
- Set up state management layer

### Wave 2: Chat Interface (T003, T004)
- Build chat UI with st.chat_message and st.chat_input
- Integrate with state management
- Add empty state handling

### Wave 3: Engine Integration (T005, T006, T007, T008)
- Connect UI to Phase 1 engine
- Implement streaming output
- Add comprehensive error handling
- Add loading states and user feedback

## Success Criteria

### Wave 1
- [ ] app.py runs without errors
- [ ] Settings sidebar displays correctly
- [ ] API keys can be entered and stored in session_state
- [ ] Keys are masked (type="password")

### Wave 2
- [ ] Chat interface displays correctly
- [ ] Chat history persists in session_state
- [ ] Empty state shows helpful message
- [ ] Input field is accessible and clear

### Wave 3
- [ ] Can send message with API keys from session_state
- [ ] Engine executes successfully
- [ ] Streaming output displays in real-time
- [ ] Error states show helpful messages
- [ ] Loading states provide clear feedback
- [ ] Complete end-to-end flow works

## Testing Matrix

- **Manual Testing**: Run `streamlit run app.py` and test all flows
- **State Persistence**: Verify session_state maintains data across reruns
- **Error Scenarios**: Test with invalid keys, network errors, empty inputs
- **Accessibility**: Keyboard navigation, screen reader compatibility
- **User Experience**: 5-second test, core task test

