import logging
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


def load_config():
    config = {
        "ROCKET_CHAT_USERNAME": os.getenv("ROCKET_CHAT_USERNAME"),
        "ROCKET_CHAT_PASSWORD": os.getenv("ROCKET_CHAT_PASSWORD"),
        "ROCKET_CHAT_SERVER_URL": os.getenv("ROCKET_CHAT_SERVER_URL"),
        "LLAMA_HOST": os.getenv("LLAMA_HOST"),
        "LLAMA_MODEL": os.getenv("LLAMA_MODEL"),
    }

    if not all(config.values()):
        logging.error("Missing one or more required environment variables.")
        raise ValueError("Environment variables are not properly set.")

    return config
