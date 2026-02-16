from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

from smartbot.core.interfaces import Message
from smartbot.providers.echo_provider import EchoProvider, OllamaConfig
from smartbot.providers.local_provider import OllamaProvider
from smartbot.providers.models import EchoConfig
from smartbot.providers.openai_provider import OpenaiProvider


@pytest.fixture
def mock_openai_client():
    client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Test response"
    client.chat.completions.create.return_value = mock_response
    return client
@pytest.fixture
def mock_openai_config():
    config = Mock()
    config.temperature = 0.7
    config.top_p = 1
    config.provider = 'openai'
    config.api_key = 'test'
    config.model_name = 'gpt-4'
    return config
def test_echoprovider_performance_test():
    """"""
    prompt = "Hola, ¿Eres tú?"
    config = EchoConfig(provider="echo")
    provider = EchoProvider(config)
    response = provider.generate_response(prompt, [])
    assert response.content == prompt

def test_generate_response(
    mock_openai_client: MagicMock,
    mock_openai_config: MagicMock
    ):
    provider = OpenaiProvider(client=mock_openai_client, config=mock_openai_config)

    prompt = Message(role="user", content="Test", timestamp=datetime.now())
    result = provider.generate_response(prompt, [])

    assert result is not None
    assert result.content == "Test response"


@patch('requests.post')
def test_generate_response_success(mock_post:MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "message": {
            "content": "¡Hola! Soy una respuesta simulada de Ollama."
        }
    }
    mock_post.return_value = mock_response

    config = OllamaConfig(
        base_url="http://localhost",
        model_name="llama3",
        temperature=0.7,
        top_p=0.9
    )

    provider = OllamaProvider(config)
    prompt = Message(role="user", content="Hola")

    result = provider.generate_response(prompt, [])

    assert result.role == "assistant"
    assert result.content == "¡Hola! Soy una respuesta simulada de Ollama."

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "http://localhost/api/chat"
    assert kwargs['json']['model'] == "llama3"
    assert not kwargs['json']['stream']
