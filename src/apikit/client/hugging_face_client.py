import os
import sys

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


def get_client(model: str) -> InferenceClient:
    token = get_token()  # Get the token
    check_token_access(model, token=token)  # Check the token can access the repo
    client = InferenceClient(model, token=token)  # Create and return the client
    return client


def get_models():
    return [
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
    ]
