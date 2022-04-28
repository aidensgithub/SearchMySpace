from tweepy import Client, Space
from typing import List
from random import shuffle
import logging as log
import time

from utilities.tools import parse_cmds_and_qrs


class SpacesAPI:
    def __init__(self, client: Client) -> None:
        super().__init__()
        self.client = client

    def get_spaces_by_keys(self, input_query: str) -> List[Space]:
        details = parse_cmds_and_qrs(input_query)
        response = self.client.search_spaces(query=details[1], space_fields=["lang"])
        return None if response.data is None else filter_spaces(response.data, details[0])


def filter_spaces(spaces: List[Space], config: dict) -> List[Space]:
    if config["state"] is not None:
        spaces = [s for s in spaces if config["state"] == s.state]
    if config["lang"] is not None:
        spaces = [s for s in spaces if config["lang"] == s.lang]
    shuffle(spaces)
    return spaces[:5]
