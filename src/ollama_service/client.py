"""Ollama API client"""

import ollama
import requests
from typing import List, Dict, Any, Optional, Generator
import json


class OllamaClient:
    """Client for interacting with Ollama API"""

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "deepseek-r1:8b"
    ):
        """
        Initialize Ollama client

        Args:
            host: Ollama server host
            model: Model name to use
        """
        self.host = host
        self.model = model
        self.client = ollama.Client(host=host)

    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def list_models(self) -> List[str]:
        """List available models"""
        try:
            response = self.client.list()
            return [model['name'] for model in response['models']]
        except Exception as e:
            raise RuntimeError(f"Failed to list models: {e}")

    def check_model_available(self) -> bool:
        """Check if the specified model is available"""
        models = self.list_models()
        return self.model in models

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        Generate response from model

        Args:
            prompt: User prompt
            system: System message
            temperature: Sampling temperature
            stream: Stream response

        Returns:
            Generated text
        """
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                system=system,
                options={"temperature": temperature},
                stream=stream
            )

            if stream:
                return response
            else:
                return response['response']
        except Exception as e:
            raise RuntimeError(f"Generation failed: {e}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Chat with model (supports function calling)

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: List of tool definitions
            temperature: Sampling temperature
            stream: Stream response

        Returns:
            Response dict
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                tools=tools,
                options={"temperature": temperature},
                stream=stream
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Chat failed: {e}")

    def generate_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        tool_executor: callable,
        max_iterations: int = 10,
        temperature: float = 0.7
    ) -> str:
        """
        Generate response with tool calling support

        Args:
            messages: Conversation messages
            tools: Available tools
            tool_executor: Function to execute tool calls
            max_iterations: Maximum tool calling iterations
            temperature: Sampling temperature

        Returns:
            Final response text
        """
        current_messages = messages.copy()
        iteration = 0

        while iteration < max_iterations:
            # Get model response
            response = self.chat(
                messages=current_messages,
                tools=tools,
                temperature=temperature
            )

            # Check if model wants to call a tool
            if 'message' in response:
                message = response['message']
                current_messages.append(message)

                # Check for tool calls
                if 'tool_calls' in message and message['tool_calls']:
                    for tool_call in message['tool_calls']:
                        tool_name = tool_call['function']['name']
                        tool_args = tool_call['function']['arguments']

                        # Execute tool
                        try:
                            tool_result = tool_executor(tool_name, tool_args)

                            # Add tool result to messages
                            current_messages.append({
                                'role': 'tool',
                                'content': json.dumps(tool_result),
                                'name': tool_name
                            })
                        except Exception as e:
                            current_messages.append({
                                'role': 'tool',
                                'content': json.dumps({"error": str(e)}),
                                'name': tool_name
                            })

                    iteration += 1
                    continue

                # No tool calls, return response
                return message.get('content', '')

            iteration += 1

        return "Max iterations reached without final response"

    def embed(self, text: str) -> List[float]:
        """
        Get embeddings for text

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings(model=self.model, prompt=text)
            return response['embedding']
        except Exception as e:
            raise RuntimeError(f"Embedding failed: {e}")
