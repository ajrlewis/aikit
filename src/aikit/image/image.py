import io
from io import BytesIO
from typing import Optional

from huggingface_hub.errors import InferenceTimeoutError, HTTPError
from loguru import logger
from PIL import Image


def text_to_image(
    client,
    prompt: str,
    negative_prompt: Optional[str] = None,
    height: Optional[float] = 1024,
    width: Optional[float] = 1024,
    num_inference_steps: Optional[float] = None,
    guidance_scale: Optional[float] = None,
    model: Optional[str] = None,
) -> Optional[io.BytesIO]:
    try:
        image = client.text_to_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            height=height,
            width=width,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            model=model,
        )
    except InferenceTimeoutError as e:
        logger.error(f"model is unavailable or the request times out: {e = }")
    except HTTPError as e:
        logger.error(
            f"request failed with an HTTP error status code other than HTTP 503: {e = }"
        )
    except Exception as e:
        logger.error(f"something went wrong: {e = }")
    else:
        return image
