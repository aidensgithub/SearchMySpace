import threading
import time
import config
from api.messages_api import DMessagesAPI
from api.spaces_api import SpacesAPI
import logging

from messenger import Messenger
from utilities.tools import find_messages_with_search_command


class Foreman:
    def __init__(self):
        self.interval = 60

        conf = config.Configurator()
        self.client_messages = DMessagesAPI(conf.create_clients()[0])
        self.client_spaces = SpacesAPI(conf.create_clients()[1])

    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()

    def run(self):
        while True:
            try:
                messages = self.client_messages.get_messages()
                messages_with_command = find_messages_with_search_command(messages)
                logging.info(f"num messages->{len(messages_with_command)}")

                for message in reversed(messages_with_command):
                    try:
                        sender_id = self.client_messages.get_sender_id(message)
                        logging.debug(f'DM from {sender_id}')
                        Messenger(message, client_m=self.client_messages, client_s=self.client_spaces)
                    except Exception as e:
                        logging.exception(e)

            except Exception as e:
                logging.exception(e)

            time.sleep(self.interval)
