import os
import sys
from typing import Optional

from huggingface_hub import auth_check, InferenceClient
from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError
from loguru import logger


def get_token():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise KeyError("HF_TOKEN environmental variable not set")
    return token


def check_token_access(model: str, token: str):
    try:
        auth_check(model, token=token)
    except GatedRepoError:
        raise GatedRepoError(f"you don't have permission to access {model = }")
    except RepositoryNotFoundError:
        raise GatedRepoError(
            f"the repository was not found or you do not have access {model = }"
        )


def get_client(model: Optional[str] = None) -> InferenceClient:
    token = get_token()  # Get the token
    if model:
        check_token_access(model, token=token)  # Check the token can access the repo
    client = InferenceClient(model, token=token)  # Create and return the client
    return client


def get_chat_models() -> list[str]:
    return [
        "meta-llama/Meta-Llama-3-8B-Instruct",
        # "meta-llama/Llama-3.1-70B-Instruct",  # requires pro subscription
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
    ]


def get_image_models() -> list[str]:
    return ["black-forest-labs/FLUX.1-schnell", "stabilityai/stable-diffusion-2-1"]
