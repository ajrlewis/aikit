import uuid

from loguru import logger


def generate_image_name(prompt):
    # Replace spaces with underscores
    prompt = prompt.replace(" ", "_")

    # Remove special characters
    prompt = "".join(e for e in prompt if e.isalnum() or e in ["_", "-", "."])

    # Add a unique identifier

    unique_id = str(uuid.uuid4())

    # Combine prompt and unique identifier
    image_name = f"{prompt}_{unique_id}.jpg"

    return image_name


def main():
    prompt = "icon icon for api service"
    image_name = generate_image_name(prompt)
    logger.debug(f"{prompt = }")
    logger.debug(f"{image_name = }")


if __name__ == "__main__":
    main()
