from loguru import logger
from typing import Optional

from . import messages
from . import prompt_templates


def completion(
    client,
    context_messages: list[dict] = [],
    model: str = None,
    max_tokens: int = 4096,
    temperature: float = 0.2,
    top_p: float = 1.0,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
) -> dict:
    """Returns the next message using a chat completion.

    Args:
        client: The inference client.
        context_messages: A list of messages.
        max_token: The maximum number of tokens allowed in the response 75 words approximately equals 100 tokens.
        temperature: Controls randomness of the generations between [0, 2]. Lower values ensure less random completions.
        top_p: Controls diversity via nucleus sampling: 0.5 means half of all likelihood-weighted options are considered.
        frequency_penalty: How much to penalize new tokens based on their existing frequency in the text so far. Decreases the model's likelihood to repeat the same line verbatim.
        presence_penalty: How much to penalize new tokens based on whether they appear in the text so far. Increases the model's likelihood to talk about new topics.
    """
    logger.debug(
        f"{model = } {max_tokens = } {temperature = } {top_p = } {frequency_penalty = } {presence_penalty = }".encode(
            "UTF-8"
        )
    )
    output = client.chat.completions.create(
        messages=context_messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    # TODO (ajrl) Add exception handling.
    choices = output.choices
    choice = choices[0]
    message = choice.message
    logger.debug(f"{message = }".encode("UTF-8"))
    content = message.content.strip()
    logger.debug(f"{content = }".encode("UTF-8"))
    message = messages.create_assistant_message(content=content)
    return message


# TODO (ajrl) call parameter change
def call(
    client,
    model: dict,
    template: dict,
    **kwargs,
) -> dict:
    """
    client: dict
      url: str
      has_access: bool
      has_chat_completions_method: bool
    model: dict
      name: str
      system: str
      params: dict
        temperature: float
        max_tokens: float
        ...
    template: dict
      name: str
      parse_json: bool
      kwargs: dict
    """
    # Render user content template
    logger.debug(f"{client = } {model = } {template = }".encode("UTF-8"))
    try:
        content = prompt_templates.render_template(template)
    except ValueError as error:
        content = f"unable to complete call, error raised: {error}"
        logger.error(f"{content = }".encode("UTF-8"))
        assistant_message = messages.create_assistant_message(content)
        logger.debug(f"{assistant_message = }".encode("UTF-8"))
        return assistant_message
    user_message = messages.create_user_message(content=content)

    # Create system context message
    system_content = model.get("system")
    if not system_content:
        system_content = "You are a helpful AI assistant."
    system_message = messages.create_system_message(content=system_content)

    # Create the context messages.
    context_messages = [system_message, user_message]

    # Get the assistant response
    try:
        assistant_message = completion(
            client,
            context_messages=context_messages,
            model=model.get("name"),
            **model.get("kwargs"),
        )
        logger.debug(f"{assistant_message = }".encode("UTF-8"))
    except Exception as e:
        content = f"unable to get completion, error raised: {e}"
        logger.error(f"{content = }".encode("UTF-8"))
        assistant_message = messages.create_assistant_message(content)
    logger.debug(f"{assistant_message = }".encode("UTF-8"))

    # Parse to JSON
    if template.get("parse_json"):
        assistant_message = messages.parse_json_content(assistant_message)

    return assistant_message
