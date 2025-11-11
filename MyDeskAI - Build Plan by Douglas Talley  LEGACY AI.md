# 

# My Desk AI
### Built by LegacyAI & Gemini

This plan is divided into two parts:
* The Agent Team Resource List: The open-source libraries your AI team will be built from.
* The Human-in-the-Loop Checklist: Your personal step-by-step "expedition" guide to gather the tools and keys needed to start Phase 1.
🤖 Agent Team Resource List (Dependencies)
This is the official list of open-source "parts" your AI agent team will need to function. The GitHub links are for your reference to check the source code and documentation.
Core Engine (The "Factory")
* crewai
  * Purpose: The main framework for building and managing your team of agents (Planner, Coder, etc.). This is the "Foreman" from our analogy.
  * GitHub URL: https://github.com/joaomdmoura/crewAI
* litellm
  * Purpose: The "Magic Translator Box." This library is critical as it lets you call over 100+ different LLMs (like Gemini, OpenAI, Kimi) using the exact same code format. This is the key to your model-agnostic "smart dispatcher."
  * GitHub URL: https://github.com/BerriAI/litellm
* langchain
  * Purpose: The underlying "language" that crewai is built on. We will specifically need langchain_community to build the "Magic Translator" wrapper.
  * GitHub URL: https://github.com/langchain-ai/langchain
Frontend (The "Control Panel")
* streamlit
  * Purpose: The Python library used to build the local, browser-based dashboard. It's perfect for creating simple UIs, like our "Settings" and "Chat" pages, without any web development experience.
  * GitHub URL: https://github.com/streamlit/streamlit
Utilities (The "Toolbelt")
* python-dotenv
  * Purpose: A simple utility to read your secret API keys from a local .env file during testing, keeping them safe and out of your source code.
  * GitHub URL: https://github.com/theskumar/python-dotenv
✅ Human-in-the-Loop Checklist (Your Expedition)
This is your step-by-step mission checklist. Complete these checkpoints, and you will be 100% ready to begin coding Phase 1.
Checkpoint 1: Set Up Your Development Environment
* [ ] 1. Install Python:
  * Goal: Ensure you have Python 3.10 or newer. This is the core language for all the tools.
  * Resource: Python 3.10.11 Download Page
* [ ] 2. Install Git:
  * Goal: The version control system for saving your work and sharing it on GitHub.
  * Resource: Git Downloads Page
* [ ] 3. Install Visual Studio Code:
  * Goal: Your code editor (the "local CLI coding platform" you mentioned).
  * Resource: VS Code Download Page
* [ ] 4. Create Project Folder & Environment:
  * Goal: Create a clean, isolated workspace for this project.
  * Action:
    * Open your terminal.
    * mkdir mydeskai
    * cd mydeskai
    * python -m venv venv (This creates the virtual environment)
    * source venv/bin/activate (On Mac/Linux) or .\venv\Scripts\activate (On Windows)
Checkpoint 2: Acquire API Keys (The "Fuel")
* [ ] 1. Get Google Gemini API Key:
  * Goal: Get your first API key. This will be the primary "brain" for your agents.
  * Resource: Google AI Studio
  * Action: Go to the URL, sign in, and click "Get API key" to create a new key.
* [ ] 2. Get OpenAI API Key:
  * Goal: Get a second, different API key. This is essential for testing our "Magic Translator" wrapper to prove it can switch between models.
  * Resource: OpenAI Platform
  * Action: Sign up, go to the "API keys" section, and create a new secret key. (Note: You may need to add a small credit (e.g., $5) to your account to activate the API).
Checkpoint 3: Final Project Kick-off
* [ ] 1. Install All Python Libraries:
  * Goal: Install all the "Agent Team Resources" into your virtual environment.
  * Action: With your environment active, run this single command:
    pip install crewai crewai[tools] litellm langchain-community streamlit python-dotenv

* [ ] 2. Create Your (Temporary) .env File:
  * Goal: Securely store your keys for local testing during Phase 1.
  * Action: In your mydeskai folder, create a new file named .env and add your keys like this:
    GEMINI_API_KEY="your-new-gemini-key-here"
OPENAI_API_KEY="your-new-openai-key-here"

* [ ] 3. Create .gitignore:
  * Goal: Tell Git to ignore your secret keys and environment files.
  * Action: Create a file named .gitignore and add this text:
    venv/
.env
__pycache__/

Once all these boxes are checked, you are officially ready to start Phase 1: Task 1.3 (building the "Magic Translator" wrapper).
This tutorial offers a helpful guide on how to get set up with Google AI Studio to create your Gemini API key.

Here is the complete project outline for "My Desk AI," designed to be the most feasible, financially responsible, and open-source-focused plan based on our entire discussion.
This plan directly incorporates the "Scrum Master's" feedback, solving the blockers before they happen to minimize technical debt.
Project: My Desk AI
* Goal: An open-source, local-first desktop dashboard for agentic AI swarms. It will provide a simple interface to define, run, and monitor teams of AI agents (like crewai) for complex coding and analysis tasks.
* Philosophy: Open-source first, minimal dependencies, low financial cost (uses your own local machine and API keys), and maintainable by a solo developer.
Phase 1: The Engine & The Wrapper (No UI Yet)
Goal: Build the "engine" of the app and solve the single hardest technical challenge first. We must prove our agents can be created and can use any "brain" (LLM) we give them. This entire phase is done in your local CLI.
* Task 1.1: Create the Project Structure
  * Create the main folder mydeskai.
  * Inside, create a Python virtual environment (e.g., python -m venv venv).
  * Create your requirements.txt file.
* Task 1.2: Install Core Dependencies
  * Add and install the "engine" libraries:
    * crewai
    * crewai[tools]
    * litellm (Our "magic translator box" for all LLMs)
    * python-dotenv (To manage API keys)
    * langchain_community (Needed for the wrapper)
* Task 1.3: Build the "Magic Translator" Wrapper (The 98% Confidence Check)
  * This is the single most important task. We must make litellm (the translator) work with crewai (the agent team).
  * Create a file named llm_wrapper.py.
  * Inside, you will write a custom Python class that "wraps" litellm so that crewai thinks it's a standard LangChain LLM. This solves the primary blocker from the original plan.
* Task 1.4: Define the "Test Crew"
  * Create agents.py: Define a simple "Test Agent" that uses your llm_wrapper.py.
  * Create tasks.py: Define a simple "Test Task" (e.g., "Tell me a joke.").
* Task 1.5: Create the "Engine" Test Script
  * Create a file named test_engine.py.
  * This script will:
    * Load your API keys from a .env file.
    * Import the wrapper, the agent, and the task.
    * Assemble and .kickoff() the crew.
  * Definition of Done: You can run python test_engine.py in your terminal and see the "Test Agent" successfully run and print a joke. This proves the core concept is sound.
Phase 2: The MVP Dashboard (The UI)
Goal: Build the actual "My Desk AI" dashboard using Streamlit. This phase imports Phase 1's code as a module, avoiding the "subprocess" blocker entirely.
* Task 2.1: Add Streamlit Dependency
  * Add streamlit to your requirements.txt and install it.
* Task 2.2: Build the Main App File
  * Create app.py. This is your Streamlit dashboard.
* Task 2.3: Implement the "Settings" Page
  * Use st.sidebar to create a "Settings" area.
  * Add st.text_input fields for API keys (Gemini, OpenAI, etc.), making sure to use type="password".
  * No .env file! This is the key to avoiding the state management bug. You will save the keys into Streamlit's st.session_state only. This is simpler and more secure.
* Task 2.4: Build the "Chat" Interface
  * Use st.chat_message and st.chat_input to create the chat UI.
  * Your chat history will also be stored in st.session_state.
* Task 2.5: Connect the UI to the Engine
  * When a user presses "Send":
    * The app.py will read the API keys from st.session_state.
    * It will read the user's prompt.
    * It will import and call your crew functions from Phase 1 (e.g., from agents import MyCrew).
    * It will pass the keys and prompt to the crew.
    * It will use st.spinner() and st.write_stream() to show the live output from the agents as they "think."
* Definition of Done: You can run streamlit run app.py, go to the webpage, enter an API key, and have a simple chat with your "Test Agent" from Phase 1.
Phase 3: Core Functionality (The "Real" Agents)
Goal: Make the agents useful by giving them the roles and tools from your original plan.
* Task 3.1: Define the "Real" Agent Roles
  * Go into agents.py and replace the "Test Agent" with your full team:
    * PlannerAgent
    * FileReaderAgent
    * CodeAnalystAgent
    * ReportWriterAgent
  * Each agent's llm will be your llm_wrapper from Phase 1.
* Task 3.2: Implement the "Smart Router"
  * In app.py, before you call the crew, create a simple function (e.g., def route_model(prompt):).
  * This function will check the prompt for keywords ("code", "write", "analyze") and pick the best LLM model name (e.g., "gemini-1.5-pro", "claude-3-haiku").
  * You will pass this model name to your crew. This achieves your "smart dispatcher" goal.
* Task 3.3: Add File System Tools
  * crewai[tools] comes with tools for reading files. In agents.py, give the FileReaderAgent the FileReadTool.
  * This allows the user to type "Analyze the file my_script.py" and the agent can actually read it.
* Definition of Done: You can now have a "real" conversation. You can ask the app to "Please read plan.md and code.py and tell me if the code meets the plan's requirements." The full agent swarm will run and give you a real answer.
Phase 4: Refinement & Community Prep
Goal: Clean up the project, add documentation, and make it ready to be shared on GitHub.
* Task 4.1: Create a README.md
  * This is your "pay it forward" moment.
  * Write a clear, simple guide:
    * What is "My Desk AI"?
    * How to install it (the pip install -r requirements.txt steps).
    * How to run it (streamlit run app.py).
    * A quick example of how to use it.
* Task 4.2: Create the .gitignore File
  * Make sure to ignore your venv/ folder, your .env file (if you still have one for testing), and any __pycache__ folders.
* Task 4.3: Final Code Cleanup
  * Add comments to your code explaining why you did things. This is invaluable for other solo devs who will learn from your project.
* Definition of Done: Your project is now on GitHub. Another developer could (in theory) find it, follow your README, and get "My Desk AI" running on their own machine.
Phase 5: The Open-Source Backlog (Future)
Goal: Create a "wishlist" of features. This invites community collaboration and gives you a clear roadmap for the future. You will add these to your GitHub "Issues" page.
* Voice Input: Integrate streamlit-webrtc for audible commands (as the Scrum Master said, save this for last).
* File Uploads: Add a Streamlit button to let users upload files instead of just giving a path.
* Agent Management: Create a new page in the UI where users can define their own agents and roles without editing the Python code.
* Cursor 2 Integration: (Optional) Investigate if Cursor 2 has an API. If so, you could add it as a "brain" in your llm_wrapper, allowing you to route tasks to it or your open-source agents.

This phased plan gives you clear, sequential wins, solves the major technical risks upfront, and builds directly toward your goal of creating a valuable, open-source project for the community.
Would you like me to help you start by drafting the code for Task 1.3: The "Magic Translator" Wrapper? It's the most critical first step.


**My Desk AI**
A simple, powerful, and local-first control panel for building, managing, and running autonomous AI agent swarms right from your desktop.
🎯 Project Goal
My Desk AI was born from a simple need: to bridge the gap between powerful, command-line AI agents and a clean, visual, human-in-the-loop workflow.
As solo developers, we often find ourselves managing dozens of complex tasks, prompts, and agent configurations from a terminal. This project provides a simple "Command and Control" dashboard, built with Streamlit, that acts as a desktop interface for your agentic coding teams.
The goal is to provide a single panel where you can:
* Visually manage your API keys and settings.
* Define complex tasks in a simple chat interface.
* Deploy swarms of AI agents (using crewai) to execute the work.
* Watch the agents work in real-time, with full streaming output.
* Leverage a "Smart Dispatcher" (powered by litellm) to automatically route the right job to the right "brain" (Gemini, Kimi, OpenAI, etc.).
Community & Future
This project is, at its core, an effort to "pay it forward."
Being a solo developer can often feel like you're on an island. You have no one to bounce ideas off of, no senior dev to ask for guidance, and no team to critique your work. The open-source community becomes that team.
Our hope is that My Desk AI becomes a useful tool for other solo devs, researchers, and hobbyists.
We are building this in the open so that:
* Others can learn from our code, our successes, and our failures.
* The community can contribute by adding new features, suggesting improvements, and making the tool more robust.
* It lowers the barrier to entry for anyone who wants to experiment with multi-agent AI systems but finds the CLI-only approach intimidating.
This project is intended to be a starting point. We invite you to fork it, build on it, and make it your own.
🙏 Acknowledgments & Gratitude
This project stands on the shoulders of giants. "My Desk AI" is not a new invention, but a new composition—an orchestration made possible only by the incredible, foundational work of the open-source community.
We are building this platform using a stack of powerful, free, and open-source tools. We owe our deepest gratitude to the creators and maintainers of these projects:
* Streamlit: For creating the most joyful, fast, and Python-native way to build data and web applications. You've made frontend development accessible to all of us.
* crewAI: For building a flexible and robust framework for agent orchestration. You've turned the complex concept of collaborative AI into a tangible, usable tool.
* LiteLLM: For solving one of the biggest headaches in AI development. Your "magic translator box" for over 100+ LLMs is a masterpiece of interoperability and a critical piece of this project.
* LangChain: For pioneering the language and framework that powers so much of the modern AI stack, including crewai. Your work has defined the blueprint for agent-based architectures.
Without these tools, this project would not be possible. We are simply connecting the dots that you so brilliantly created.
Thank you.
License
My Desk AI is licensed under the MIT License. You are free to use, modify, and distribute this project as you see fit.
