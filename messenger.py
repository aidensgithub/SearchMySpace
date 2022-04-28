import threading
import logging
import time

from tweepy import Client

from api.messages_api import DMessagesAPI
from api.spaces_api import SpacesAPI


class Messenger:

    def __init__(self, message_received, client_m: DMessagesAPI, client_s: SpacesAPI):
        self.message_received = message_received
        self.client_m = client_m
        self.client_s = client_s

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        logging.info(f'run Messenger')
        sender_id = self.client_m.get_sender_id(self.message_received)
        spaces = self.client_s.get_spaces_by_keys(self.message_received.message_create['message_data']["text"])
        if spaces is None:
            spaces = ["No Spaces found for this request :("]
        fail_counter = 0
        success_counter = 0
        for s in spaces:
            try:
                s = s if isinstance(s, str) else "https://www.twitter.com/i/spaces/"+s.id
                reply = self.client_m.send_message(s, sender_id)
                if reply is not None and (reply.id is not None or reply.created_timestamp is not None):
                    success_counter += 1
                time.sleep(2)
                logging.info(f'Sending to: {sender_id} message: {s}')
                self.client_m.delete_message(reply.id)
            except Exception as e:
                fail_counter += 1
                logging.info(f'Error {e}')

        if fail_counter <= success_counter:
            self.client_m.delete_message(self.message_received.id)

