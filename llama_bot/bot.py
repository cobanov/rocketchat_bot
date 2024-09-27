import logging
import time

from requests import sessions

from llama_bot import RocketChatBot, load_config, setup_logging

config = load_config()
setup_logging()


def run_bot():
    with sessions.Session() as session:
        bot = RocketChatBot(session, config)

        while True:
            try:
                bot.run(channel="GENERAL")

                time.sleep(3)

            except Exception as e:
                logging.error(f"Unexpected error occurred: {e}")
                time.sleep(10)

if __name__ == "__main__":
    run_bot()
