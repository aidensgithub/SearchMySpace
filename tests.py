import config
from api.messages_api import DMessagesAPI

conf = config.Configurator()
api = conf.create_api()
x = api.media_upload('search_hint.gif', media_category='dm_gif', shared=True)
print(x)

# aa = DMessagesAPI(api)
# aa.setup_default_welcome()
# messages = api.get_direct_messages(count=5)
# print(messages)
# for message in reversed(messages):
#     sender_id = message.message_create["sender_id"]
#
#     text = message.message_create["message_data"]["text"]
#     print(text)


