# My Desk AI

A simple, powerful, and local-first control panel for building, managing, and running autonomous AI agent swarms right from your desktop.

## 🎯 Project Goal

My Desk AI was born from a simple need: to bridge the gap between powerful, command-line AI agents and a clean, visual, human-in-the-loop workflow.

As solo developers, we often find ourselves managing dozens of complex tasks, prompts, and agent configurations from a terminal. This project provides a simple "Command and Control" dashboard, built with Streamlit, that acts as a desktop interface for your agentic coding teams.

The goal is to provide a single panel where you can:
* Visually manage your API keys and settings.
* Define complex tasks in a simple chat interface.
* Deploy swarms of AI agents (using crewai) to execute the work.
* Watch the agents work in real-time, with full streaming output.
* Leverage a "Smart Dispatcher" (powered by litellm) to automatically route the right job to the right "brain" (Gemini, Kimi, OpenAI, etc.).

## 🚀 Quick Start

### Prerequisites

* Python 3.10 or newer
* Git (for version control)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd MyDeskAI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Mac/Linux:
   source venv/bin/activate
   
   # On Windows:
   .\venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your API keys:**
   Create a `.env` file in the project root with your API keys:
   ```env
   GEMINI_API_KEY="your-gemini-key-here"
   OPENAI_API_KEY="your-openai-key-here"
   ```

### Running the Engine Test (Phase 1)

To test the core engine:

```bash
python test_engine.py
```

This will run a simple test that creates a test agent and task, proving the core concept works.

### Running the Dashboard (Phase 2)

Once Phase 2 is implemented:

```bash
streamlit run app.py
```

## 📁 Project Structure

```
MyDeskAI/
├── llm_wrapper.py      # Magic Translator Wrapper (Task 1.3)
├── agents.py           # Agent definitions
├── tasks.py            # Task definitions
├── test_engine.py      # Engine test script (Task 1.5)
├── app.py              # Streamlit dashboard (Phase 2)
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🏗️ Development Phases

### Phase 1: The Engine & The Wrapper ✅
- [x] Project structure
- [x] Core dependencies
- [x] Magic Translator Wrapper
- [x] Test crew setup
- [x] Engine test script

### Phase 2: The MVP Dashboard (Coming Soon)
- [ ] Streamlit integration
- [ ] Settings page
- [ ] Chat interface
- [ ] UI-to-engine connection

### Phase 3: Core Functionality (Coming Soon)
- [ ] Real agent roles (Planner, FileReader, CodeAnalyst, ReportWriter)
- [ ] Smart router/dispatcher
- [ ] File system tools

### Phase 4: Refinement & Community Prep (Coming Soon)
- [ ] Documentation
- [ ] Code cleanup
- [ ] GitHub preparation

## 🙏 Acknowledgments

This project stands on the shoulders of giants. We are deeply grateful to:

* **Streamlit**: For making frontend development accessible
* **crewAI**: For building a flexible framework for agent orchestration
* **LiteLLM**: For the "magic translator box" supporting 100+ LLMs
* **LangChain**: For pioneering the language and framework that powers modern AI stacks

## 📄 License

My Desk AI is licensed under the MIT License. You are free to use, modify, and distribute this project as you see fit.

## 🤝 Contributing

This project is built in the open for the community. We welcome contributions, suggestions, and improvements!

---

**Built by LegacyAI & Gemini**

