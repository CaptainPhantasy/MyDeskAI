"""
Comprehensive test suite for tools integration
Tests tool registry, tool selector, and agent tool assignment.
"""

import sys
from tools_registry import (
    get_all_tools,
    get_tool_set,
    get_tools_by_category,
    get_category_info,
    TOOL_CATEGORIES,
    TOOL_SETS,
    SHELL_TOOL_AVAILABLE,
    S3_TOOLS_AVAILABLE,
    MCP_AVAILABLE,
)
from tool_selector import get_tool_selector
from agents import (
    create_test_agent,
    create_file_reader_agent,
    create_code_analyst_agent,
)
from llm_wrapper import LiteLLMWrapper


def test_tools_registry():
    """Test tools registry functionality."""
    print("Testing tools registry...")
    
    # Test get_all_tools
    all_tools = get_all_tools()
    assert len(all_tools) > 0, "Should have tools available"
    print(f"  ✅ Total tools: {len(all_tools)}")
    
    # Test get_category_info
    category_info = get_category_info()
    assert len(category_info) > 0, "Should have categories"
    print(f"  ✅ Categories: {len(category_info)}")
    
    # Test get_tool_set
    minimal_set = get_tool_set("minimal")
    assert len(minimal_set) > 0, "Minimal set should have tools"
    print(f"  ✅ Minimal tool set: {len(minimal_set)} tools")
    
    # Test get_tools_by_category
    file_tools = get_tools_by_category("file_operations")
    assert len(file_tools) > 0, "Should have file operation tools"
    print(f"  ✅ File operations category: {len(file_tools)} tools")
    
    print("  ✅ Tools registry tests passed\n")


def test_tool_selector():
    """Test tool selector functionality."""
    print("Testing tool selector...")
    
    selector = get_tool_selector()
    
    # Test file-related prompt
    analysis = selector.analyze_prompt("Read app.py and summarize it")
    assert analysis["primary_category"] == "file_operations", "Should detect file operations"
    assert analysis["confidence"] >= 2, "Should have good confidence"
    print(f"  ✅ File prompt analysis: {analysis['primary_category']} (confidence: {analysis['confidence']})")
    
    # Test code-related prompt
    analysis = selector.analyze_prompt("Analyze the code in main.py for bugs")
    # Code prompts might match file_operations too (due to .py), so check if code_development is in matched categories
    assert "code_development" in analysis.get("matched_categories", []) or analysis["primary_category"] == "code_development", "Should detect code development"
    print(f"  ✅ Code prompt analysis: {analysis['primary_category']} (matched: {analysis.get('matched_categories', [])})")
    
    # Test tool selection
    tools = selector.select_tools("Read app.py", max_tools=3)
    assert len(tools) > 0, "Should select tools"
    print(f"  ✅ Tool selection: {len(tools)} tools selected")
    
    print("  ✅ Tool selector tests passed\n")


def test_agent_tool_assignment():
    """Test agent tool assignment."""
    print("Testing agent tool assignment...")
    
    llm = LiteLLMWrapper(model_name="gpt-3.5-turbo")
    
    # Test file reader agent
    file_agent = create_file_reader_agent(llm, "gpt-3.5-turbo")
    assert len(file_agent.tools) > 0, "File reader agent should have tools"
    print(f"  ✅ File reader agent: {len(file_agent.tools)} tools")
    
    # Test code analyst agent
    code_agent = create_code_analyst_agent(llm, "gpt-3.5-turbo")
    assert len(code_agent.tools) > 0, "Code analyst agent should have tools"
    print(f"  ✅ Code analyst agent: {len(code_agent.tools)} tools")
    
    # Test test agent with tools
    selector = get_tool_selector()
    tools = selector.select_tools("Read a file", max_tools=2)
    test_agent = create_test_agent(llm, "gpt-3.5-turbo", tools=tools)
    print(f"  ✅ Test agent with tools: {len(test_agent.tools)} tools")
    
    print("  ✅ Agent tool assignment tests passed\n")


def test_tool_availability():
    """Test tool availability flags."""
    print("Testing tool availability...")
    
    print(f"  ✅ Shell tool available: {SHELL_TOOL_AVAILABLE}")
    print(f"  ✅ S3 tools available: {S3_TOOLS_AVAILABLE}")
    print(f"  ✅ MCP available: {MCP_AVAILABLE}")
    
    print("  ✅ Tool availability tests passed\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("TOOLS INTEGRATION TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        test_tools_registry()
        test_tool_selector()
        test_agent_tool_assignment()
        test_tool_availability()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

