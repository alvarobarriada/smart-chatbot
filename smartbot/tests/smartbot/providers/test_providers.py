from smartbot.providers.echo_provider import EchoProvider
from smartbot.providers.models import EchoConfig



def test_echoprovider_performance_test():
    prompt = "Hola, ¿Eres tú?"
    config = EchoConfig(provider="echo")
    provider = EchoProvider(config)
    response = provider.generate_response(prompt, [])
    assert response.content == prompt

