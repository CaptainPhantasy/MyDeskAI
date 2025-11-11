"""
Smart Router - Task 3.2
Intelligently routes tasks to the best LLM model based on prompt analysis.
"""


def route_model(prompt: str, available_models: list) -> str:
    """
    Route a prompt to the best available model based on content analysis.
    
    Args:
        prompt: The user's prompt/question
        available_models: List of available model names
        
    Returns:
        The best model name for this task
    """
    prompt_lower = prompt.lower()
    
    # Default to first available model
    if not available_models:
        return "glm-4.6"  # Default to GLM-4.6 if available
    
    # Prioritize GLM-4.6 (user's preferred model)
    if "glm-4.6" in available_models:
        return "glm-4.6"
    
    # Code-related tasks - prefer models good at code
    code_keywords = ["code", "program", "function", "class", "script", "debug", "analyze code", "review code"]
    if any(keyword in prompt_lower for keyword in code_keywords):
        # Prefer GLM-4.6 for code, then GPT models
        for model in available_models:
            if "glm" in model.lower():
                return model
            if "gpt" in model.lower():
                return model
        return available_models[0]
    
    # Writing tasks - prefer GLM-4.6, then GPT models
    write_keywords = ["write", "create", "generate", "draft", "compose", "story", "article"]
    if any(keyword in prompt_lower for keyword in write_keywords):
        for model in available_models:
            if "glm" in model.lower():
                return model
            if "gpt" in model.lower():
                return model
        return available_models[0]
    
    # Analysis tasks - prefer GLM-4.6, then GPT models
    analysis_keywords = ["analyze", "compare", "evaluate", "assess", "review", "examine"]
    if any(keyword in prompt_lower for keyword in analysis_keywords):
        for model in available_models:
            if "glm" in model.lower():
                return model
            if "gpt" in model.lower():
                return model
        return available_models[0]
    
    # File reading tasks - prefer GLM-4.6
    file_keywords = ["read", "file", "open", "load"]
    if any(keyword in prompt_lower for keyword in file_keywords):
        for model in available_models:
            if "glm" in model.lower():
                return model
        return available_models[0]
    
    # Default: prefer GLM-4.6, then first available model
    for model in available_models:
        if "glm" in model.lower():
            return model
    return available_models[0]

