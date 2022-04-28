from nltk import word_tokenize
import re


# deprecated
def sanitize_tokens(input_query) -> str:
    return "".join([word + " " for word in word_tokenize(input_query) if word.isalpha()])


def parse_cmds_and_qrs(input_query: str):
    match_state = re.search("(\*\w+)", input_query)
    match_lang = re.search("(#\w+)", input_query)
    config = {
        "state": match_state.group().strip("*") if match_state is not None else None,
        "lang": match_lang.group().strip("#") if match_lang is not None else None,
    }
    query = input_query if match_state is None else input_query.replace(match_state.group(), "")
    query = query if match_lang is None else query.replace(match_lang.group(), "")
    return config, query


def find_messages_with_search_command(messages: list):
    messages_with_command = []
    for m in messages:
        match = re.search("(\/search+)", m.message_create['message_data']['text'])
        if match is not None and len(m.message_create['message_data']['entities']['urls']) == 0:
            m.message_create['message_data']['text'] = m.message_create['message_data']['text'] \
                .replace(match.group(), "")
            messages_with_command.append(m)

    return messages_with_command
