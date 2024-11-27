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
parse_json = "Convert and return this data into valid working JSON: `{data}`"

language = "What is the primary language of his text: `{text}`."
translate = "Translate this text from `{from_language}` to `{to_language}`: `{text}`"

PROMPT_NAME_TO_TEMPALTE = {
    "ask": ask,
    "extract": extract,
    "summarize": summarize,
    "sentiment": sentiment,
    "code": code,
    "keywords": keywords,
    "humanize": humanize,
    "parse_json": parse_json,
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


def render_template(template: dict) -> Optional[str]:
    logger.debug(f"{template = }")
    template_name = template.get("name")
    template_kwargs = template.get("kwargs", {})
    template_parse_json = template.get("parse_json")
    prompt_template = _get(template_name)
    if content := _render(prompt_template, **template_kwargs):
        content = f"{content} {REMOVE_COMMENTS}"
        if template_parse_json:
            content = f"{content} {JSON_FORMAT}"
        return content


def main():
    template = {
        "name": "extract",
        "kwargs": {
            "text": "While Microsoft owns GitHub, it does not have complete control over the codebase of a potential competitor or acquisition target that uses GitHub for hosting their entire codebase. This is because GitHub is a separate company with its own CEO and legal entity, and Microsoft's acquisition of GitHub did not include the purchase of the codebase of other companies using the platform. Additionally, open-source projects like Git, which GitHub is built upon, are licensed under the GPLv2 and cannot be purchased by a single entity. Instead, contributors to these projects agree to distribute their work under the same license.",
            "data_points": {"summary": "A summary of the text."},
        },
        "parse_json": False,
    }
    content = render_template(template)
    logger.debug(f"{content = }")


if __name__ == "__main__":
    main()
