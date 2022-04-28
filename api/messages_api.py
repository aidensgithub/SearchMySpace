from tweepy import API


class DMessagesAPI:
    def __init__(self, api: API) -> None:
        super().__init__()
        self.client = api

    def get_messages(self):
        messages = self.client.get_direct_messages(count=50)
        return messages

    def get_sender_id(self, message):
        sender_id = message.message_create["sender_id"]
        return sender_id

    def send_message(self, message, sender_id):
        return self.client.send_direct_message(sender_id, message)

    def delete_message(self, message_id):
        return self.client.delete_direct_message(message_id)


    def setup_default_welcome(self,  **kwargs):
        json_payload = {
            "welcome_message": {
                "name": "Welcome instruction message",
                "message_data": {
                    "text": "Welcome dear! To search for Spaces, press search and enter the search keywords delimited with space"
                }
            }
        }
        return self.client.request('POST', 'direct_messages/welcome_messages/new',
                                   json_payload=json_payload, payload_type='json', **kwargs)
