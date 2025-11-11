"""
Engine Test Script - Task 1.5
This script tests the core engine by loading API keys, creating agents and tasks,
and running a test crew.
"""

import os
from dotenv import load_dotenv
from crewai import Crew
from llm_wrapper import LiteLLMWrapper
from agents import create_test_agent
from tasks import create_test_task

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main test function that assembles and runs the test crew.
    """
    print("🚀 My Desk AI - Engine Test")
    print("=" * 50)
    
    # Get API keys from environment
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not gemini_key and not openai_key:
        print("❌ Error: No API keys found in .env file")
        print("Please create a .env file with at least one of:")
        print("  GEMINI_API_KEY=your-key-here")
        print("  OPENAI_API_KEY=your-key-here")
        return
    
    # Set the API key for litellm (it will use the appropriate one based on model)
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    
    # Choose model based on available keys
    # Note: Using OpenAI for initial testing. Gemini requires additional setup.
    if openai_key:
        model_name = "gpt-3.5-turbo"
        print(f"✅ Using model: {model_name} (OpenAI)")
    elif gemini_key:
        # Use litellm format for Gemini - try gemini-1.5-flash or gemini-pro
        model_name = "gemini/gemini-1.5-flash"
        print(f"✅ Using model: {model_name} (Gemini)")
    else:
        model_name = "gpt-3.5-turbo"
    
    # Create the LLM wrapper
    llm = LiteLLMWrapper(
        model_name=model_name,
        temperature=0.7,
    )
    
    # Create the test agent
    agent = create_test_agent(llm)
    
    # Create the test task
    task = create_test_task(agent, "Tell me a joke.")
    
    # Assemble the crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )
    
    # Run the crew
    print("\n🤖 Starting crew execution...")
    print("-" * 50)
    result = crew.kickoff()
    
    print("\n" + "=" * 50)
    print("✅ Test Complete!")
    print("=" * 50)
    print("\nResult:")
    print(result)


if __name__ == "__main__":
    main()

