from typing import Optional

from loguru import logger

REMOVE_COMMENTS = "**Your response will be sent directly to my client, so do not include comments directed toward me, e.g. `Here are the ...`, etc.**"
JSON_FORMAT = "**Return your response as valid JSON.**"

ask = "{question}"
extract = "Analyze the following text: `{text}`. Extract only the following data points as valid JSON: `{data_points}`. If you're not able to extract a data point, return '' for its value."
summarize = "Summarize the following text: `{text}`."
sentiment = "Determine the sentiment from the following text: `{text}`. Return only 'positive', 'neutral' or 'negative'."
code = "Generate code in the following language `{language}` to do the following: `{description}`. Return only the code in your response."
keywords = "Extract only the most relevant keywords and key phrases from this text: `{text}`. Return only the comma-separated extraction."
humanize = "Humanize the following text: `{text}`. Incorporate human-like nuances, expressions, and a natural flow, delivering content that feels genuinely human-authored."
explain = "Explain in depth what is meant by the following text: {text}"
parse_json = "Convert and return this data into valid working JSON: `{data}`"

language = "What is the primary language of his text: `{text}`."
translate = "Translate this text from `{from_language}` to `{to_language}`: `{text}`"

intent = "Identify the intent behind the following text: {text}"
stopword_removal = (
    "Remove common stopwords that do not add much value from the following text: {text}"
)
stemming = "Reduce each word to its base form in the following text: {text}"
lemmatization = "Reduce each word to its base form that can be found in a dictionary in the following text: {text}"
named_entity_recognition = 'Identify and categorize the named entities (e.g. [{ "category": "", "text": "", "type": ""}, ...]) in the following text: {text}'


PROMPT_NAME_TO_TEMPALTE = {
    "ask": ask,
    "extract": extract,
    "summarize": summarize,
    "sentiment": sentiment,
    "code": code,
    "keywords": keywords,
    "humanize": humanize,
    "parse_json": parse_json,
    "intent": intent,
    "stopword_removal": stopword_removal,
    "stemming": stemming,
    "lemmatization": lemmatization,
    "named_entity_recognition": named_entity_recognition,
}


def _get(template_name: str) -> Optional[str]:
    template = PROMPT_NAME_TO_TEMPALTE.get(template_name)
    if not template:
        message = f"{template_name = } is not supported.".encode("UTF-8")
        logger.error(message)
        raise ValueError(message)
    logger.debug(f"{template_name = } {template = }".encode("UTF-8"))
    return template


def _render(template: str, **kwargs) -> Optional[str]:
    if template:
        return template.format(**kwargs)


def render_template(template: dict) -> Optional[str]:
    logger.debug(f"{template = }".encode("UTF-8"))
    template_name = template.get("name")
    template_kwargs = template.get("kwargs", {})
    template_parse_json = template.get("parse_json")
    prompt_template = _get(template_name)
    if content := _render(prompt_template, **template_kwargs):
        content = f"{content} {REMOVE_COMMENTS}"
        if template_parse_json:
            content = f"{content} {JSON_FORMAT}"
        return content
