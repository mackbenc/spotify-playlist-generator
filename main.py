import logging
import os
import sys
import json
import pandas as pd

from utils import playlist_helper
from utils import spotify_auth
from utils import data_maker
from utils import get_refresh_token

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

USERNAME = os.environ["USERNAME"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
CODE = os.environ["CODE"]
SCOPES = ["playlist-modify-private"]
PLAYLIST_NAME = input("Name of the playlist you want to generate to\nIt can be an existing one: ")
playlist_size = 50




def playlist_generator(headers):
    playlist_id = playlist_helper.create_or_get_playlist(
        headers=headers, username=USERNAME, playlist_name=PLAYLIST_NAME
    )

    df = pd.read_json("data/final_file/data.json", orient="split")
    records = df.sample(n=playlist_size, weights=df.cnt)

    counter = playlist_helper.save_data_to_playlist(df=records, headers=headers, playlist_id=playlist_id)

    logger.info(f"inserted {playlist_size-counter} out of {playlist_size}")

if __name__ == "__main__":
    check_refresh_token_file = os.path.isfile("refresh_token.json")
    if check_refresh_token_file != True:
        logger.info("Generating refresh_token.json file")
        get_refresh_token.get_refresh_token(
            client_id=CLIENT_ID, 
            client_secret=CLIENT_SECRET, 
            code=CODE, 
            redirect_uri=REDIRECT_URI
        )
    else:
        logger.info("refresh_token.json file already exists. Token generating skipped")

    refresh_token = json.load(open('refresh_token.json'))["refresh_token"]

    token = spotify_auth.get_token(
        username=USERNAME,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        refresh_token=refresh_token,
        scopes=SCOPES,
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    check_data_file = os.path.isfile("data/final_file/data.json")
    if check_data_file != True:
        logger.info("Generating data.json file")
        data_maker.final_file_generator()
    else:
        logger.info("data.json file already exists. Data generating skipped")

    playlist_generator(headers=headers)
    