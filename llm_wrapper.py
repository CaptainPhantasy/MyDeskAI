"""
Magic Translator Wrapper - Task 1.3
This module wraps litellm so that crewai thinks it's a standard LangChain LLM.
This solves the primary blocker from the original plan.
"""

from typing import Any, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
import litellm


class LiteLLMWrapper(BaseChatModel):
    """
    A wrapper class that makes litellm compatible with crewai's LangChain-based architecture.
    This allows crewai agents to use any LLM supported by litellm (Gemini, OpenAI, GLM-4.6, etc.)
    through a unified interface.
    """
    
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    api_base: Optional[str] = None  # Custom API base URL for GLM-4.6 and other providers
    api_key: Optional[str] = None  # API key for the model
    
    @property
    def _llm_type(self) -> str:
        """Return identifier of LLM type."""
        return "litellm_wrapper"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Generate a chat response from the LLM.
        
        Args:
            messages: List of message objects
            stop: Optional list of stop sequences
            run_manager: Optional callback manager
            **kwargs: Additional arguments to pass to litellm
            
        Returns:
            ChatResult containing the generated message
        """
        try:
            # Convert LangChain messages to litellm format
            litellm_messages = []
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    litellm_messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    litellm_messages.append({"role": "assistant", "content": msg.content})
                else:
                    # Default to user message for other types
                    litellm_messages.append({"role": "user", "content": str(msg.content)})
            
            # Prepare parameters for litellm
            # For GLM-4.6, use OpenAI-compatible format with custom endpoint
            # Official API: https://api.z.ai/api/paas/v4/chat/completions
            # Model name: "glm-4.6"
            # Authentication: Bearer token in Authorization header
            if self.model_name == "glm-4.6" and self.api_base:
                # GLM-4.6 uses OpenAI-compatible API format
                # LiteLLM uses "openai/" prefix to route to OpenAI-compatible endpoints
                params = {
                    "model": "openai/glm-4.6",  # LiteLLM format for OpenAI-compatible APIs
                    "messages": litellm_messages,
                    "temperature": self.temperature,
                    "api_base": self.api_base,  # Base URL: https://api.z.ai/api/paas/v4
                }
                if self.api_key:
                    params["api_key"] = self.api_key  # Bearer token authentication
            else:
                # Standard litellm format
                params = {
                    "model": self.model_name,
                    "messages": litellm_messages,
                    "temperature": self.temperature,
                }
                
                # Add API base URL if provided (for custom endpoints)
                if self.api_base:
                    params["api_base"] = self.api_base
                
                # Add API key if provided
                if self.api_key:
                    params["api_key"] = self.api_key
            
            if self.max_tokens:
                params["max_tokens"] = self.max_tokens
            
            if stop:
                params["stop"] = stop
            
            # Merge any additional kwargs
            params.update(kwargs)
            
            # Call litellm
            response = litellm.completion(**params)
            
            # Extract the text from the response
            if response and response.choices:
                message_content = response.choices[0].message.content
                message = AIMessage(content=message_content)
                generation = ChatGeneration(message=message)
                return ChatResult(generations=[generation])
            else:
                message = AIMessage(content="")
                generation = ChatGeneration(message=message)
                return ChatResult(generations=[generation])
                
        except Exception as e:
            raise Exception(f"Error calling litellm with model {self.model_name}: {str(e)}")
    
    @property
    def _identifying_params(self) -> dict:
        """Return identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_base": self.api_base,
        }

