import json
import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


def final_file_generator():
    check_data_file = os.path.isfile("data/final_file/count_data.json")
    if check_data_file == True:
        logger.info("data.json file already exists. Data generating skipped")
        return
    logger.info("Generating data.json file")
    df = pd.DataFrame(
        columns=[
            "ts",
            "username",
            "ms_played",
            "track_name",
            "artist_name",
            "album_name",
            "spotify_track_uri",
            "shuffle",
            "skipped",
        ]
    )

    data_path = "data/all_history"
    out_data_path = "data/final_file"

    for filename in os.listdir(data_path):
        if filename == ".gitkeep":
            continue
        filepath = os.path.join(data_path, filename)
        # checking if it is a file
        f = open(filepath)
        file = json.load(f)

        dfItem = pd.DataFrame.from_records(file)
        dfItem = dfItem.rename(
            columns={
                "master_metadata_track_name": "track_name",
                "master_metadata_album_artist_name": "artist_name",
                "master_metadata_album_album_name": "album_name",
            }
        )

        dfItem = dfItem[
            [
                "ts",
                "username",
                "ms_played",
                "track_name",
                "artist_name",
                "album_name",
                "spotify_track_uri",
                "shuffle",
                "skipped",
            ]
        ]

        dfItem["ts"] = pd.to_datetime(dfItem["ts"])
        df = pd.concat([df, dfItem], ignore_index=True)

    df = df.drop_duplicates()

    df.to_json(out_data_path + "/all_data.json", orient="split", compression="infer")

    df = df.groupby(
        [
            "artist_name",
            "track_name",
            "album_name",
            "spotify_track_uri",
        ]
    ).count()
    df = df.rename(columns={"ms_played": "cnt"})
    df = df.reset_index()

    df.to_json(out_data_path + "/count_data.json", orient="split", compression="infer")

    check_data_file = os.path.isfile("data/final_file/count_data.json")
    if check_data_file != True:
        logger.info("Generating data.json file")
        data_maker.final_file_generator()
    else:
        logger.info("data.json file already exists. Data generating skipped")
