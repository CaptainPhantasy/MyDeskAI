# Testing Guide - My Desk AI Phase 2

## Quick Start Testing

### 1. Start the Dashboard

```bash
cd /Volumes/Storage/Development/MyDeskAI
source venv/bin/activate
streamlit run app.py
```

The app should open in your browser at `http://localhost:8501`

---

## Step-by-Step Testing Procedure

### Test 1: Initial State Check ✅

**What to verify:**
- [ ] Dashboard loads without errors
- [ ] Sidebar is visible on the left
- [ ] Main chat area is visible
- [ ] No API keys are configured (shows warning/error state)

**Expected behavior:**
- Settings sidebar shows "❌ No API keys configured"
- Chat input is visible but disabled/not functional
- No chat history displayed

---

### Test 2: API Key Configuration ✅

**Steps:**
1. In the sidebar, locate the "API Keys" section
2. Enter your OpenAI API key in the "OpenAI API Key" field
   - Key should be masked (password type)
   - Get key from: https://platform.openai.com/api-keys
3. Optionally enter Gemini API key
   - Get key from: https://aistudio.google.com/app/apikey

**What to verify:**
- [ ] Keys are accepted (no immediate error)
- [ ] Status changes to "✅ Ready" when at least one key is entered
- [ ] Model selection dropdown appears with available models
- [ ] Keys persist when you refresh the page (session state)

**Expected behavior:**
- Status indicator turns green
- Model dropdown shows available options (e.g., "gpt-3.5-turbo" if OpenAI key is set)
- No error messages

---

### Test 3: Model Selection ✅

**Steps:**
1. With at least one API key configured
2. Use the "Select Model" dropdown in sidebar
3. Choose a model (e.g., "gpt-3.5-turbo")

**What to verify:**
- [ ] Model selection works
- [ ] Selected model persists in session state
- [ ] Model name is correct format

**Expected behavior:**
- Dropdown shows available models based on configured keys
- Selection is saved

---

### Test 4: Basic Chat Interaction ✅

**Steps:**
1. Ensure at least one API key is configured
2. Select a model from dropdown
3. In the chat input at bottom, type: "Tell me a joke"
4. Press Enter or click Send

**What to verify:**
- [ ] User message appears in chat immediately
- [ ] Loading spinner appears ("🤔 Agent is thinking...")
- [ ] Agent response appears after processing
- [ ] Response is coherent and relevant
- [ ] Chat history persists (both messages visible)

**Expected behavior:**
- User message shows in chat with "user" avatar
- Assistant message appears with "assistant" avatar
- Response should be a joke (or relevant to the prompt)
- No errors in console or UI

---

### Test 5: Chat History Persistence ✅

**Steps:**
1. After Test 4, send another message: "What's 2+2?"
2. Verify both messages are in history
3. Refresh the browser page (F5 or Cmd+R)

**What to verify:**
- [ ] Chat history persists across page refreshes
- [ ] All previous messages are visible
- [ ] API keys are still configured

**Expected behavior:**
- All chat messages remain visible after refresh
- Session state maintains data

---

### Test 6: Clear Chat History ✅

**Steps:**
1. Have some chat history (from previous tests)
2. Click "🗑️ Clear Chat History" button in sidebar
3. Verify chat is cleared

**What to verify:**
- [ ] Chat history is cleared
- [ ] Only new messages appear after clearing
- [ ] API keys remain configured

**Expected behavior:**
- Chat area becomes empty
- Can start fresh conversation
- Settings remain intact

---

### Test 7: Error Handling - Invalid API Key ✅

**Steps:**
1. Enter an invalid API key (e.g., "test-key-12345")
2. Select a model
3. Try to send a message

**What to verify:**
- [ ] Error message appears in chat
- [ ] Error is user-friendly (not raw exception)
- [ ] App doesn't crash
- [ ] Can correct the key and retry

**Expected behavior:**
- Error message like "❌ Error: [descriptive error]"
- Chat interface remains functional
- Can update key and try again

---

### Test 8: Error Handling - No API Keys ✅

**Steps:**
1. Clear all API keys (delete from input fields)
2. Try to send a message

**What to verify:**
- [ ] Warning/error message appears
- [ ] Message: "Please configure at least one API key..."
- [ ] Chat doesn't attempt to process

**Expected behavior:**
- Clear error message
- No processing attempt
- User can add keys and retry

---

### Test 9: Model Switching ✅

**Steps:**
1. Configure both OpenAI and Gemini keys
2. Send a message with "gpt-3.5-turbo" selected
3. Switch to "gemini/gemini-1.5-flash" in dropdown
4. Send another message

**What to verify:**
- [ ] Model switch works
- [ ] Different model processes the request
- [ ] Responses may differ (different models)

**Expected behavior:**
- Model selection updates
- New requests use selected model
- Both models work if keys are valid

---

### Test 10: Multiple Messages in Sequence ✅

**Steps:**
1. Send several messages in a row:
   - "Hello"
   - "What can you do?"
   - "Tell me about AI"
2. Verify each response

**What to verify:**
- [ ] Each message is processed correctly
- [ ] Chat history shows all messages in order
- [ ] No state corruption
- [ ] Performance is acceptable

**Expected behavior:**
- All messages appear in order
- Each gets a response
- No errors or crashes

---

## Advanced Testing

### Test 11: Streaming Output (If Supported) ✅

**Steps:**
1. Send a longer prompt that requires more processing
2. Watch for real-time streaming output

**What to verify:**
- [ ] Text appears incrementally (if streaming works)
- [ ] Or complete response appears at once (if streaming not yet working)
- [ ] No errors during streaming

**Note:** Streaming may need refinement based on crewai event system.

---

### Test 12: Long Responses ✅

**Steps:**
1. Ask for a detailed response: "Write a short story about a robot"
2. Verify long responses display correctly

**What to verify:**
- [ ] Long text is properly formatted
- [ ] Chat scrolls appropriately
- [ ] No UI overflow issues

---

## Troubleshooting

### Issue: App won't start

**Check:**
- Virtual environment is activated: `source venv/bin/activate`
- Streamlit is installed: `pip list | grep streamlit`
- Port 8501 is available

**Fix:**
```bash
pip install streamlit
streamlit run app.py --server.port 8502  # Use different port
```

---

### Issue: "No module named 'crewai'"

**Check:**
- Virtual environment is activated
- Dependencies are installed

**Fix:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### Issue: API key not working

**Check:**
- Key is correct (no extra spaces)
- Key has proper permissions
- Account has credits/quota

**Fix:**
- Verify key in provider dashboard
- Test key with simple API call
- Check account status

---

### Issue: Agent not responding

**Check:**
- API key is configured correctly
- Model is selected
- Check browser console for errors
- Check terminal output for errors

**Fix:**
- Verify key format
- Try different model
- Check network connection
- Review error messages

---

## Success Criteria

Phase 2 is successful if:

✅ Dashboard loads without errors  
✅ API keys can be configured and saved  
✅ Model selection works  
✅ Chat interface is functional  
✅ Agent responds to messages  
✅ Chat history persists  
✅ Error handling works gracefully  
✅ Clear chat function works  
✅ Multiple messages work in sequence  

---

## Performance Benchmarks

**Expected:**
- App startup: < 3 seconds
- Message processing: 5-30 seconds (depends on model/API)
- UI responsiveness: Immediate
- Memory usage: Reasonable (< 500MB)

---

## Next Steps After Testing

If all tests pass:
- ✅ Phase 2 is complete
- 🚀 Ready for Phase 3 (Real Agent Roles)

If issues found:
- Document issues in `shared-docs/issues.md`
- Fix critical bugs
- Re-test affected areas

---

## Quick Test Command

Run this to verify basic setup:

```bash
cd /Volumes/Storage/Development/MyDeskAI
source venv/bin/activate
python -c "import streamlit; import crewai; from llm_wrapper import LiteLLMWrapper; print('✅ All imports successful')"
```

If this passes, you're ready to test the dashboard!

