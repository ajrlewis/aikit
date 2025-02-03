import json

from loguru import logger

from . import chat
from . import messages
from . import prompt_templates


def ask(
    client,
    model: str,
    question: str,
    temperature: float = 0.3,
    parse_json: bool = False,
) -> dict:
    logger.debug(f"{question = }")
    model_data = {
        "name": model,
        "system": "You are a helpful AI assistant.",
        "kwargs": {"temperature": temperature},
    }
    template_data = {
        "name": "ask",
        "kwargs": {"question": question},
        "parse_json": parse_json,
    }
    assistant_message = chat.call(client, model=model_data, template=template_data)
    logger.debug(assistant_message)
    data = assistant_message.get("content", {})
    logger.debug(f"{data = }")
    return data


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


def summarize(client, model: str, text: str, temperature: float = 0.1) -> str:
    model_data = {
        "name": model,
        "system": "You return a comprehensive summary of a given text only.",
        "kwargs": {"temperature": temperature},
    }
    template_data = {"name": "summarize", "kwargs": {"text": text}}
    assistant_message = chat.call(client, model=model_data, template=template_data)
    summary = assistant_message.get("content", "")
    logger.info(f"{summary = }")
    return summary


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


def named_entity_recognition(
    client, model: str, text: str, temperature: float = 0.3
) -> str:
    model_data = {
        "name": model,
        "system": "You compute named entity recognition of text.",
        "kwargs": {"temperature": temperature},
    }
    template_data = {
        "name": "named_entity_recognition",
        "kwargs": {"text": text},
        "parse_json": True,
    }
    assistant_message = chat.call(client, model=model_data, template=template_data)
    named_entities = assistant_message.get("content", "")
    logger.debug(f"{named_entities = }")
    return named_entities
