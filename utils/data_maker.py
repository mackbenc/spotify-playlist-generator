import json
import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


def final_file_generator():
    """Reads our raw history files to a dataframe, aggregates, transforms it 
    and saves it out as a json file
    """

    # Check if out file exists. If yes the whole data generation is skipped
    check_data_file = os.path.isfile("data/final_file/count_data.json")
    if check_data_file == True:
        logger.info("data.json file already exists. Data generating skipped")
        return
    
    logger.info("Generating data.json file")

    # Creating an empty dataframe with the correct columns
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

    # Paths to our files
    data_path = "data/all_history"
    out_data_path = "data/final_file"

    # Iterate through the files in our all_history folder
    for filename in os.listdir(data_path):
        if filename == ".gitkeep":
            continue
        filepath = os.path.join(data_path, filename)
        f = open(filepath)
        file = json.load(f)

        dfItem = pd.DataFrame.from_records(file)

        # Renaming the columns to our schema
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

        # Convert the ts column to the proper type
        dfItem["ts"] = pd.to_datetime(dfItem["ts"])
        # Append the content of the file to a final dataframe
        df = pd.concat([df, dfItem], ignore_index=True)

    # dropping duplicates
    df = df.drop_duplicates()

    # Save out the file containing all of our history as a Json file
    df.to_json(out_data_path + "/all_data.json", orient="split", compression="infer")

    # Aggregating
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

    # Save dataframe to a json file containing the our aggregated history with counts per track
    df.to_json(out_data_path + "/count_data.json", orient="split", compression="infer")

