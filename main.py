import json
import logging
import os
import sys

import pandas as pd

from utils import data_maker, get_refresh_token, playlist_helper

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

USERNAME = os.environ["USERNAME"]


PLAYLIST_NAME = input(
    "Name of the playlist you want to generate to\nIt can be an existing one: "
)
playlist_size = int(input("How many records to insert (max 100): "))


def playlist_generator(headers):
    playlist_id = playlist_helper.create_or_get_playlist(
        headers=headers, username=USERNAME, playlist_name=PLAYLIST_NAME
    )

    df = pd.read_json("data/final_file/count_data.json", orient="split")
    records = df.sample(n=playlist_size, weights=df.cnt)

    playlist_helper.save_data_to_playlist(
        df=records, headers=headers, playlist_id=playlist_id
    )


if __name__ == "__main__":
    headers = get_refresh_token.get_header(username=USERNAME)

    data_maker.final_file_generator()

    playlist_generator(headers=headers)
