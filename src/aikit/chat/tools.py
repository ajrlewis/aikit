import json

from loguru import logger

from . import chat
from . import messages
from . import prompt_templates


def keywords(client, model: str, text: str, temperature: float = 0.3) -> str:
    model_data = {
        "name": model,
        "system": "You extract keywords from text only.",
        "kwargs": {"temperature": temperature},
    }
    template_data = {"name": "keywords", "kwargs": {"text": text}}
    assistant_message = chat.call(client, model=model_data, template=template_data)
    keywords = assistant_message.get("content", "")
    logger.info(f"{keywords = }")
    return keywords


def intent(client, model: str, text: str, temperature: float = 0.3) -> str:
    model_data = {
        "name": model,
        "system": "You return the one-word intent of a given text only.",
        "kwargs": {"temperature": temperature},
    }
    template_data = {"name": "intent", "kwargs": {"text": text}}
    assistant_message = chat.call(client, model=model_data, template=template_data)
    intent = assistant_message.get("content", "")
    logger.info(f"{intent = }")
    return intent
