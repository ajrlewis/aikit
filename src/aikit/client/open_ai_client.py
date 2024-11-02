import os

import openai
from openai import AuthenticationError


def get_token():
    token = os.getenv("OPENAI_API_KEY")
    if not token:
        raise KeyError("OPENAI_API_KEY environmental variable not set")
    return token


def check_token_access(client: openai.OpenAI):
    try:
        _ = client.models.list()
    except AuthenticationError as e:
        raise AuthenticationError(f"you don't have permission to access this API.")


def get_client() -> openai.OpenAI:
    api_key = get_token()  # Get the token
    client = openai.OpenAI(api_key=api_key)
    check_token_access(client)
    # if not hasattr(client, "chat_completion"):
    #     client.chat_completion = client.chat.completions.create
    return client


def get_models():
    return ["gpt-3.5-turbo", "gpt-4"]
