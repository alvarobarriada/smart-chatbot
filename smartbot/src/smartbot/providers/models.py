from typing import Annotated, Literal
from pydantic import BaseModel, Field, SecretStr

class BaseConfig(BaseModel):
    """Settings shared with each model"""
    temperature: float = 0.7
    top_p: int = 40

class OpenAIConfig(BaseConfig):
    """Settings for OpenAI"""
    provider: Literal["openai"] = "openai"
    api_key: SecretStr
    model_name: str = "gpt-4o"

class OllamaConfig(BaseConfig):
    """Settings for ollama"""
    provider: Literal["ollama"] = "ollama"
    base_url: str = "http://localhost:11434"
    model_name: str = "llama3.2:1b"
class EchoConfig(BaseConfig):
    """Settings for echo"""
    provider: Literal["echo"]="echo"

ModelConfig = Annotated[
    OpenAIConfig| OllamaConfig|EchoConfig,
    Field(discriminator="provider")
]

class ChatBotConfig(BaseModel):
    """Tu configuración global del bot"""
    bot_name: str
    llm: ModelConfig
