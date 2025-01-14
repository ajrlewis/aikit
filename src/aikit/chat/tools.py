import json

from loguru import logger

from . import chat
from . import messages
from . import prompt_templates


def extract(
    client, model: str, text: str, data_points: dict, temperature: float = 0.3
) -> dict:
    logger.debug(f"{text = } {data_points = }")
    model_data = {
        "name": model,
        "system": "You extract JSON data points from text.",
        "kwargs": {"temperature": temperature},
    }
    template_data = {
        "name": "extract",
        "kwargs": {"text": text, "data_points": data_points},
        "parse_json": True,
    }
    assistant_message = chat.call(client, model=model_data, template=template_data)
    logger.debug(assistant_message)
    data = assistant_message.get("content", {})
    logger.debug(f"{data = }")
    return data


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
