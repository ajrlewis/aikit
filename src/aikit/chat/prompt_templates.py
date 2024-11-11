from typing import Optional

from loguru import logger

ask = "{question}"
extract = "Extract (or infer) these data points: `{data_points}` from the following text: `{text}`. If you're not able to extract a data point, return '' for it's value. Finally, return only the extracted data points as a JSON object in your response. Do not format your response in any other way."
summarize = "Summarize the following text: `{text}`. Return only the summary of the text in your response."
sentiment = "Determine the sentiment from the following text: `{text}`. Return only 'positive', 'negative' or 'neutral' depending on the sentiment. Do not include any other text."
code = "Generate code in the following language `{language}` to do the following: `{description}`. Return only the code in your response. Do not include any other text."
keywords = "Analyze this text: `{text}. Return only the comma-separated keywords for the text. Do not include any other text in your response."
humanize = "Analyze the following text: `{text}`. Transform it into a human-like version, incorporating vocabulary variation, sentence structure adjustments, and natural language patterns to make it indistinguishable from human-written content. Return only the formatted text in your response. Do not format your response."


slogan = "Generate a slogan for company called `{name} ({description})`. Return only the slogan in your response."
paragraph = "Generate a website paragraph for company called `{name} ({description})`. Return only the paragraph in your response."
condense = "Analyze this text: `{text}`. Condense the text into a maximum of {number_of_words} words. Return only the condensed text in your response."
language = "What language is this text in: {text}. Return only the language. Do not format your response."
translate = ""
rewrite = ""

PROMPT_NAME_TO_TEMPALTE = {
    "summarize": summarize,
    "extract": extract,
    "sentiment": sentiment,
    "code": code,
    "slogan": slogan,
    "paragraph": paragraph,
    "condense": condense,
    "keywords": keywords,
    "ask": ask,
    "humanize": humanize,
    "language": language,
    "translate": translate,
    "rewrite": rewrite,
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
        return content
