import json
import re

from loguru import logger


def create_message(role: str, content: str) -> dict:
    return {"role": role, "content": content}


def create_user_message(content: str) -> dict:
    return create_message(role="user", content=content)


def create_assistant_message(content: str) -> dict:
    return create_message(role="assistant", content=content)


def create_system_message(content: str) -> dict:
    return create_message(role="system", content=content)


def parse_json_content(message: dict) -> dict:
    content = message.get("content", "")
    logger.debug(f"{content = }".encode("UTF-8"))
    try:
        content = content.replace("`", "")
        content = re.sub(r'\\(?![nrtbf"\'\\])', r"\\\\", content)
        message["content"] = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"failed to parse message content to JSON: {e = }".encode("UTF-8"))
    return message
