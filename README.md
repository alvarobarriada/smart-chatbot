# 🤖 Smart-ChatBot 🤖

**Smart-ChatBot** es un motor de chatbot diseñado para ser versátil y fácil de configurar. Permite alternar entre modelos locales (vía Ollama) y modelos en la nube (vía OpenAI) con solo cambiar un archivo de configuración, manteniendo una interfaz consistente para el usuario.

## Requisitos previos

Antes de empezar, asegúrate de tener instalado:

- [uv](https://github.com/astral-sh/uv): Gestor de paquetes y entornos de Python ultra rápido.
- Ollama: si planeas usar modelos locales.

---

## Instalación y configuración

Sigue estos pasos para poner en marcha tu instancia de SmartBot:

1. Clonar el repositorio e instalar dependencias
Desde la carpeta raíz del proyecto, ejecuta el siguiente comando para sincronizar el entorno y las dependencias:

```cmd
uv sync
```

2. Configuración del entorno (`.env`)
Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave de API si vas a utilizar OpenAI:

```cmd
api_key_openai=<API_KEY>
```

3. Configuración del bot (`config.yaml`)
El archivo `config.yaml` es el corazón de la configuración. Aquí puedes definir qué cerebro usará tu bot:

```YAML
bot_name: SmartBot

llm:
  provider: ollama        # Opciones: 'ollama' o 'openai'
  base_url: http://localhost:11434  # Requerido solo para Ollama
  model_name: llama3.2:1b # El modelo específico a ejecutar
  temperature: 0.7        # Creatividad del modelo (0.0 a 1.0)
```

---

## Uso del proyecto

Para iniciar el chatbot, una vez configurado el entorno, simplemente ejecuta:

```cmd
uv run python main.py
```

## Documentación de la configuración (API Interna)

El sistema utiliza una lógica de discernimiento basada en el campo `provider`. A continuación se detallan los parámetros:

| **Parámetro** | **Tipo** | **Descripción**                                                                                                   |
| ------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `bot_name`    | String   | El nombre con el que el bot se identificará en la consola.                                                        |
| `provider`    | String   | **El selector clave.** Determina la clase encargada de la comunicación (`ollama` para local, `openai` para nube). |
| `base_url`    | URL      | Endpoint del servidor local. Solo es procesado si el provider es `ollama`.                                        |
| `model_name`  | String   | Identificador del modelo (ej: `gpt-4o`, `llama3.2:1b`, `mistral`).                                                |
| `temperature` | Float    | Controla la aleatoriedad. Valores bajos son más precisos; altos son más creativos.                                |
| `top_p`       | Float    | Define el umbral de probabilidad acumulada para la selección de tokens.                                           |

---

## Ejemplo de uso

Si configuras el `provider` como `ollama` y el `model_name` como `llama3.2:1b` al ejecutar el programa verás algo como esto:

```cmd
SmartBot CLI — type /exit to quit.
>
```

¡Ya estás preparado para hablar con el smart-chatbot!

```cmd
SmartBot CLI — type /exit to quit.
> ¡Hola smartbot! Cuéntame algo sobre ti: qué modelo usas, cuál es tu proveedor, qué se te puede preguntar...
¡Hola! Me alegra que me hayas preguntado eso.

Soy un modelo de lenguaje grande (LLM) llamado Llama. Llama significa "Meta-Llama". Fui desarrollado por Meta, y he sido entrenado en una gran cantidad de texto para que pueda entender y generar lenguaje humano.

Me puedo preguntar:

* ¿Qué te gustaría saber sobre mí?
* ¿Cuál es tu pregunta favorita sobre mí o otros tópicos?
* ¿Hay algo específico que me desees saber o discutir?

Puedes intentarlo con una de las siguientes preguntas, o tienes alguna otra idea en mente. Estoy aquí para ayudarte!
>
```
