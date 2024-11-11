from typing import Optional

from loguru import logger

REMOVE_FORMATTING = "Your response will be sent directly to my client, so do not include comments directed toward me."

ask = "{question}"
extract = "Extract (or infer) these data points: `{data_points}` from the following text: `{text}`. If you're not able to extract a data point, return '' for it's value. Return only the extracted data points as a JSON object in your response."
summarize = "Summarize the following text: `{text}`."
sentiment = "Determine the sentiment from the following text: `{text}`. Return only 'positive', 'neutral' or 'negative'."
code = "Generate code in the following language `{language}` to do the following: `{description}`. Return only the code in your response."
keywords = "Extract only the most relevant keywords and key phrases from this text: `{text}`. Return only the comma-separated extraction."
humanize = "Humanize the following text: `{text}`. Incorporate human-like nuances, expressions, and a natural flow, delivering content that feels genuinely human-authored."

# slogan = "Generate a slogan for company called `{name} ({description})`. Return only the slogan in your response."
# paragraph = "Generate a website paragraph for company called `{name} ({description})`. Return only the paragraph in your response."
# language = "What language is this text in: {text}. Return only the language. Do not format your response."
# translate = ""
# rewrite = ""

PROMPT_NAME_TO_TEMPALTE = {
    "ask": ask,
    "extract": extract,
    "summarize": summarize,
    "sentiment": sentiment,
    "code": code,
    "keywords": keywords,
    "humanize": humanize,
}


def _get(template_name: str) -> Optional[str]:
    template = PROMPT_NAME_TO_TEMPALTE.get(template_name)
    if not template:
        message = f"{template_name = } is not supported."
        logger.error(message)
        raise ValueError(message)
    logger.debug(f"{template_name = } {template = }")
    return template


def _render(template: str, **kwargs) -> Optional[str]:
    if template:
        return template.format(**kwargs)


def render_template(template_name: str, **kwargs) -> Optional[str]:
    template = _get(template_name)
    content = _render(template, **kwargs)
    if content:
        return f"{content} {REMOVE_FORMATTING}"
