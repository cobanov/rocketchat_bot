import logging

from rocketchat_API.rocketchat import RocketChat

from .llama_client import LlamaClient


class RocketChatBot:
    def __init__(self, session, config):
        self.username = config["ROCKET_CHAT_USERNAME"]
        self.server_url = config["ROCKET_CHAT_SERVER_URL"]

        self.rocket = RocketChat(
            config["ROCKET_CHAT_USERNAME"],
            config["ROCKET_CHAT_PASSWORD"],
            server_url=config["ROCKET_CHAT_SERVER_URL"],
            session=session,
        )
        self.llama_client = LlamaClient(config)

    def get_last_message(self, channel, count=1):
        try:
            response = self.rocket.channels_history(channel, count=count).json()
            return response.get("messages", [None])[0]
        except Exception as e:
            logging.error(f"Error fetching message history: {e}")
            return None

    def get_mentions(self, message):
        return [mention.get("name") for mention in message.get("mentions", [])]

    def clean_message(self, message):
        usernames = ["LlamaBot", "llamabot"]
        msg_text = message.get("msg", "")
        for username in usernames:
            msg_text = msg_text.replace(f"@{username}", "").strip()
        return msg_text

    def handle_llamabot_mention(self, message, sender):
        user_message = self.clean_message(message)

        try:
            response_message = self.llama_client.process_message(user_message)
            logging.info(f"LlamaBot response: {response_message}")

            self.rocket.chat_post_message(
                f"@{sender}, {response_message}", channel="GENERAL"
            )
        except Exception as e:
            logging.error(f"Error processing LlamaBot response: {e}")
            self.rocket.chat_post_message(
                f"@{sender}, Sorry, I encountered an error processing your request.",
                channel="GENERAL",
            )

    def run(self, channel="GENERAL"):
        last_message = self.get_last_message(channel)
        if not last_message:
            logging.info("No new messages found.")
            return

        mentions = self.get_mentions(last_message)
        if "LlamaBot" in mentions:
            sender = last_message.get("u").get("username")
            if sender != self.username:
                self.handle_llamabot_mention(last_message, sender)
