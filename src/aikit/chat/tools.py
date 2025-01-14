import json

from loguru import logger

from . import messages
from . import prompt_templates


def intent(client, model: str, text: str, temperature: float = 0.3) -> str:
    model_data = {
        "name": model,
        "system": "You return the one-word intent of a given text only.",
        "kwargs": {"temperature": temperature},
    }
    template_data = {"name": "intent", "kwargs": {"text": query}, "parse_json": True}
    assistant_message = chat.call(client, model=model_data, template=template_data)
    intent = assistant_message.get("content", "")
    logger.info(f"{intent = }")
    return intent
