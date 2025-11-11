"""
Complete System Test - Tests all Claude Code components
"""

import sys
from command_recognizer import get_command_recognizer
from decision_engine import get_decision_engine
from handler_dispatcher import get_dispatcher
from file_operations_handler import get_file_handler
from code_generation_handler import get_code_handler
from git_handler import get_git_handler
from search_handler import get_search_handler
from terminal_handler import get_terminal_handler
from error_handling_cascades import get_error_handler
from output_formatter import get_output_formatter
from meta_logic import get_meta_logic
from agent_orchestrator import get_orchestrator
from tools_registry import get_all_tools, get_category_info


def test_all_components():
    """Test all components."""
    print("=" * 70)
    print("COMPLETE SYSTEM TEST - CLAUDE CODE IMPLEMENTATION")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Command Recognizer
    print("Test 1: Command Recognizer")
    tests_total += 1
    try:
        recognizer = get_command_recognizer()
        result = recognizer.classify_input("Read app.py")
        assert result["intent"] is not None
        assert result["confidence"] > 0
        print("  ✅ Command recognition works")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed: {e}")
    
    # Test 2: Decision Engine
    print("\nTest 2: Decision Engine")
    tests_total += 1
    try:
        engine = get_decision_engine()
        result = engine.process_request("Read app.py")
        assert result.get("task_type") is not None
        assert result.get("tools") is not None
        print("  ✅ Decision engine works")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed: {e}")
    
    # Test 3: Handler Dispatcher
    print("\nTest 3: Handler Dispatcher")
    tests_total += 1
    try:
        dispatcher = get_dispatcher()
        result = dispatcher.dispatch("Read app.py")
        assert result.get("decision") is not None
        print("  ✅ Handler dispatcher works")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed: {e}")
    
    # Test 4: All Handlers
    print("\nTest 4: All Handlers")
    handlers = [
        ("File", get_file_handler),
        ("Code", get_code_handler),
        ("Git", get_git_handler),
        ("Search", get_search_handler),
        ("Terminal", get_terminal_handler),
        ("Error", get_error_handler),
        ("Output", get_output_formatter),
        ("Meta", get_meta_logic),
        ("Orchestrator", get_orchestrator),
    ]
    
    for name, get_handler in handlers:
        tests_total += 1
        try:
            handler = get_handler()
            assert handler is not None
            print(f"  ✅ {name} handler initialized")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ {name} handler failed: {e}")
    
    # Test 5: Tools Registry
    print("\nTest 5: Tools Registry")
    tests_total += 1
    try:
        all_tools = get_all_tools()
        category_info = get_category_info()
        assert len(all_tools) > 0
        assert len(category_info) > 0
        print(f"  ✅ Tools registry: {len(all_tools)} tools, {len(category_info)} categories")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {tests_passed}/{tests_total} tests passed")
    print("=" * 70)
    
    if tests_passed == tests_total:
        print("✅ ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL")
        return True
    else:
        print(f"⚠️ {tests_total - tests_passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = test_all_components()
    sys.exit(0 if success else 1)

