"""
Code Generation Handler - Section 3 of Claude Code Plan
Handles code generation, component creation, and implementation
"""

from typing import Dict, List, Any, Optional
import re
from file_operations_handler import get_file_handler


class CodeGenerationHandler:
    """Handles code generation following Claude Code logic."""
    
    def __init__(self):
        """Initialize code generation handler."""
        self.file_handler = get_file_handler()
    
    def generate_component(self, component_type: str, name: str, framework: Optional[str] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate a component following Section 3.1 logic.
        
        Args:
            component_type: Type of component (react, vue, api, model, etc.)
            name: Component name
            framework: Framework to use
            context: Optional context
            
        Returns:
            Generation result
        """
        # COMPONENT TYPE DETECTION
        detected_type = self._detect_component_type(component_type, name, context)
        
        # TEMPLATE SELECTION
        template = self._select_template(detected_type, framework, context)
        
        # GENERATION EXECUTION
        files = self._generate_files(name, template, detected_type, context)
        
        return {
            "success": True,
            "component_type": detected_type,
            "name": name,
            "files_created": files,
            "template": template["name"]
        }
    
    def generate_function(self, function_spec: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate a function following Section 3.2 logic.
        
        Args:
            function_spec: Function specification
            context: Optional context
            
        Returns:
            Generation result
        """
        # FUNCTION ANALYSIS
        analysis = self._analyze_function(function_spec)
        
        # IMPLEMENTATION STRATEGY
        implementation = self._generate_implementation(analysis, context)
        
        # INTEGRATION
        integration = self._integrate_function(implementation, context)
        
        return {
            "success": True,
            "function": implementation,
            "analysis": analysis,
            "integration": integration
        }
    
    def generate_class(self, class_spec: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate a class following Section 3.3 logic.
        
        Args:
            class_spec: Class specification
            context: Optional context
            
        Returns:
            Generation result
        """
        # ARCHITECTURE DECISION
        architecture = self._decide_architecture(class_spec)
        
        # MEMBER GENERATION
        members = self._generate_members(class_spec, architecture)
        
        # MODULE STRUCTURE
        module = self._create_module_structure(class_spec, members, context)
        
        return {
            "success": True,
            "class": module,
            "architecture": architecture,
            "members": members
        }
    
    def _detect_component_type(self, component_type: str, name: str, context: Optional[Dict]) -> str:
        """Detect component type from specification."""
        component_lower = component_type.lower()
        
        if any(word in component_lower for word in ["react", "component", "jsx"]):
            return "react_component"
        elif any(word in component_lower for word in ["vue", "sfc"]):
            return "vue_component"
        elif any(word in component_lower for word in ["api", "endpoint", "route"]):
            return "api_endpoint"
        elif any(word in component_lower for word in ["model", "schema", "entity"]):
            return "data_model"
        else:
            return "generic_component"
    
    def _select_template(self, component_type: str, framework: Optional[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Select appropriate template."""
        templates = {
            "react_component": {
                "name": "React Component",
                "content": self._react_template(),
                "extension": ".jsx"
            },
            "api_endpoint": {
                "name": "API Endpoint",
                "content": self._api_template(),
                "extension": ".py"
            },
            "data_model": {
                "name": "Data Model",
                "content": self._model_template(),
                "extension": ".py"
            },
            "generic_component": {
                "name": "Generic Component",
                "content": self._generic_template(),
                "extension": ".py"
            }
        }
        
        return templates.get(component_type, templates["generic_component"])
    
    def _generate_files(self, name: str, template: Dict, component_type: str, context: Optional[Dict]) -> List[str]:
        """Generate files for component."""
        files = []
        
        # Generate main file
        file_name = f"{name}{template['extension']}"
        content = template["content"].replace("{name}", name).replace("{Name}", name.capitalize())
        
        result = self.file_handler.create_file(file_name, content, context)
        if result["success"]:
            files.append(file_name)
        
        # Generate test file if needed
        if component_type in ["react_component", "api_endpoint"]:
            test_file = f"{name}_test{template['extension']}"
            test_content = self._generate_test_content(name, component_type)
            result = self.file_handler.create_file(test_file, test_content, context)
            if result["success"]:
                files.append(test_file)
        
        return files
    
    def _analyze_function(self, function_spec: Dict) -> Dict[str, Any]:
        """Analyze function specification."""
        return {
            "purpose": function_spec.get("purpose", "utility"),
            "complexity": self._assess_complexity(function_spec),
            "signature": self._design_signature(function_spec)
        }
    
    def _generate_implementation(self, analysis: Dict, context: Optional[Dict]) -> str:
        """Generate function implementation."""
        signature = analysis["signature"]
        complexity = analysis["complexity"]
        
        if complexity == "simple":
            return f"def {signature}:\n    # Simple implementation\n    pass\n"
        elif complexity == "medium":
            return f"def {signature}:\n    \"\"\"Function docstring.\"\"\"\n    try:\n        # Implementation\n        pass\n    except Exception as e:\n        raise\n"
        else:
            return f"def {signature}:\n    \"\"\"Complex function implementation.\"\"\"\n    # Error handling\n    try:\n        # Main logic\n        pass\n    except Exception as e:\n        # Error handling\n        raise\n    finally:\n        # Cleanup\n        pass\n"
    
    def _assess_complexity(self, function_spec: Dict) -> str:
        """Assess function complexity."""
        if function_spec.get("lines", 0) < 10:
            return "simple"
        elif function_spec.get("lines", 0) < 50:
            return "medium"
        else:
            return "complex"
    
    def _design_signature(self, function_spec: Dict) -> str:
        """Design function signature."""
        name = function_spec.get("name", "function")
        params = function_spec.get("parameters", [])
        param_str = ", ".join(params) if params else ""
        return f"{name}({param_str})"
    
    def _decide_architecture(self, class_spec: Dict) -> Dict[str, Any]:
        """Decide class architecture."""
        return {
            "pattern": class_spec.get("pattern", "standard"),
            "inheritance": class_spec.get("inheritance", None),
            "responsibility": "single"
        }
    
    def _generate_members(self, class_spec: Dict, architecture: Dict) -> Dict[str, Any]:
        """Generate class members."""
        return {
            "properties": class_spec.get("properties", []),
            "methods": class_spec.get("methods", []),
            "lifecycle": class_spec.get("lifecycle", [])
        }
    
    def _create_module_structure(self, class_spec: Dict, members: Dict, context: Optional[Dict]) -> str:
        """Create module structure."""
        class_name = class_spec.get("name", "MyClass")
        properties = members.get("properties", [])
        methods = members.get("methods", [])
        
        code = f"class {class_name}:\n"
        code += '    """Class docstring."""\n\n'
        
        # Properties
        for prop in properties:
            code += f"    {prop} = None\n\n"
        
        # Methods
        for method in methods:
            code += f"    def {method}(self):\n        pass\n\n"
        
        return code
    
    def _react_template(self) -> str:
        """React component template."""
        return """import React from 'react';

const {Name} = () => {
  return (
    <div>
      <h1>{name}</h1>
    </div>
  );
};

export default {Name};
"""
    
    def _api_template(self) -> str:
        """API endpoint template."""
        return """from fastapi import APIRouter

router = APIRouter()

@router.get("/{name}")
async def get_{name}():
    \"\"\"Get {name}.\"\"\"
    return {{"message": "{name}"}}

@router.post("/{name}")
async def create_{name}(data: dict):
    \"\"\"Create {name}.\"\"\"
    return {{"message": "Created", "data": data}}
"""
    
    def _model_template(self) -> str:
        """Data model template."""
        return """from pydantic import BaseModel
from typing import Optional

class {Name}(BaseModel):
    \"\"\"{name} model.\"\"\"
    id: Optional[int] = None
    name: str
    
    class Config:
        orm_mode = True
"""
    
    def _generic_template(self) -> str:
        """Generic component template."""
        return """\"\"\"
{name} component
\"\"\"

class {Name}:
    \"\"\"{name} class.\"\"\"
    
    def __init__(self):
        pass
"""
    
    def _generate_test_content(self, name: str, component_type: str) -> str:
        """Generate test file content."""
        return f"""import pytest
from {name} import {name.capitalize()}

def test_{name}():
    \"\"\"Test {name}.\"\"\"
    # Test implementation
    pass
"""


# Global instance
_code_handler = None

def get_code_handler() -> CodeGenerationHandler:
    """Get or create global code generation handler."""
    global _code_handler
    if _code_handler is None:
        _code_handler = CodeGenerationHandler()
    return _code_handler

