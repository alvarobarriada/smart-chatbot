import pytest
from pydantic import SecretStr, ValidationError

from smartbot.providers.models import (
    BaseConfig,
    ChatBotConfig,
    OllamaConfig,
    OpenAIConfig,
)


def test_base_config_valid_ranges():
    """Verify that it accepts correct values within the limits."""
    config = BaseConfig(temperature=0.0, top_p=1.0)
    assert config.temperature == 0.0
    assert config.top_p == 1.0

@pytest.mark.parametrize("param, value", [
    ("temperature", -0.1),
    ("temperature", 1.1),
    ("top_p", -0.1),
    ("top_p", 1.1),
])
def test_base_config_invalid_ranges(param:str, value:float):
    """Verify that throw error if values are out of range."""
    with pytest.raises(ValidationError):
        BaseConfig(**{param: value})


# --- Tests de Providers Específicos ---

def test_openai_config_secret_key():
    """Ensure that API Key be handled as an API key."""
    config = OpenAIConfig(api_key=SecretStr("sk-test-123"))
    assert isinstance(config.api_key, SecretStr)
    # Al imprimirlo no debería verse la clave real
    assert "**********" in str(config.api_key)
    assert config.api_key.get_secret_value() == "sk-test-123"

def test_ollama_config_defaults():
    """Verify values by default for Ollama."""
    config = OllamaConfig()
    assert config.provider == "ollama"
    assert config.base_url == "http://localhost:11434"
    assert "llama" in config.model_name


def test_chatbot_config_discriminator_openai():
    """Try that discriminator create a OpenAIConfig correctly."""
    data = {
        "bot_name": "TestBot",
        "llm": {
            "provider": "openai",
            "api_key": "secret-key"
        }
    }
    config = ChatBotConfig(**data)
    assert isinstance(config.llm, OpenAIConfig)
    assert config.llm.model_name == "gpt-4o"

def test_chatbot_config_discriminator_ollama():
    """Try that discriminator create a OllamaConfig correctly."""
    data = {
        "bot_name": "TestBot",
        "llm": {
            "provider": "ollama",
            "model_name": "phi3"
        }
    }
    config = ChatBotConfig(**data)
    assert isinstance(config.llm, OllamaConfig)
    assert config.llm.model_name == "phi3"

def test_chatbot_config_invalid_provider():
    """Must throw error if provider don't exist in Union."""
    data = {
        "bot_name": "TestBot",
        "llm": {
            "provider": "anthropic",
            "model_name": "claude-3"
        }
    }
    with pytest.raises(ValidationError) :
        ChatBotConfig(**data)
