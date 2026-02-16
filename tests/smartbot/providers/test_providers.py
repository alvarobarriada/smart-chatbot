import pytest
from smartbot.providers.echo_provider import EchoProvider
from smartbot.providers.models import EchoConfig
from openai import AuthenticationError, RateLimitError


def test_echoprovider_performance_test():
    """"""
    prompt = "Hola, ¿Eres tú?"
    config = EchoConfig(provider="echo")
    provider = EchoProvider(config)
    response = provider.generate_response(prompt, [])
    assert response.content == prompt

def test_openai_generate_response_success(mocker, openai_provider):
    """"""
    # 1. Creamos un Mock para la respuesta de OpenAI
    mock_response = mocker.Mock()
    mock_response.choices = [
        mocker.Mock(message=mocker.Mock(content="Hola, soy IA"))
    ]
    # 2. "Parcheamos" el método del cliente
    # Nota: Ajusta la ruta según cómo importes el cliente en tu provider
    mocker.patch("openai.resources.chat.completions.Completions.create", return_value=mock_response)
    response = openai_provider.generate_response("Hola", [])
    assert response.content == "Hola, soy IA"
    assert response.role == "assistant"


def test_openai_handle_auth_error(mocker, openai_provider):
    mocker.patch(
        "openai.resources.chat.completions.Completions.create",
        side_effect=AuthenticationError("Invalid API Key", response=mocker.Mock(), body=None)
    )
    with pytest.raises(Exception) as excinfo:
        openai_provider.generate_response("Hola", [])

    assert "Invalid API Key" in str(excinfo.value)
