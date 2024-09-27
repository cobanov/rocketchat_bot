import logging

from ollama import Client


class LlamaClient:
    def __init__(self, config):
        self.llama_host = config["LLAMA_HOST"]
        self.llama_model = config["LLAMA_MODEL"]
        self.client = Client(host=self.llama_host)

    def process_message(self, message):
        try:
            response = self.client.chat(
                model=self.llama_model, messages=[{"role": "user", "content": message}]
            )
            return response["message"]["content"]
        except Exception as e:
            logging.error(f"Error processing message with Llama model: {e}")
            raise
