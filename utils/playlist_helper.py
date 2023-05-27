import logging

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def _get_playlists(headers, username, limit=50) -> tuple:
    """Checks if the playlist already exists. If it exists it gets the id
    for it. If it does not exists it sends a post request to create it.

    
    Parameters
    ----------
    headers : dict
        Headers variable containing the token for authorization
    username : str
        Our username
    limit : int, optional
        The number that we want the response of playlists limit to


    Returns
    -------
    tuple
        returns a tuple containig two elements
        playlist_list: 
            a list of the playlist names
        response: 
            the response we got back from the get request
    """
    logger.info("Getting playlists")
    # get all playlists
    response = requests.get(
        f"https://api.spotify.com/v1/users/{username}/playlists?limit={limit}",
        headers=headers,
        timeout=5,
    )
    if response.status_code == 200:
        logger.info("Getting playlists successful")
    else:
        logger.error("Could not get playlists:" + response.content)
        raise Exception("Could not get playlists")
    
    # Get the list of playlists from the response
    playlist_list = [pl.get("name") for pl in response.json().get("items")]
    
    return (playlist_list, response)


def create_or_get_playlist(headers, playlist_name, username) -> str:
    """Checks if the playlist already exists. If it exists it gets the id
    for it. If it does not exists it sends a post request to create it.

    
    Parameters
    ----------
    headers : dict
        Headers variable containing the token for authorization
    playlist_name : str
        The name of the playlist we want to create/get
    username : str
        Our username


    Returns
    -------
    str
        a string containing the id of the playlist
    """
    
    playlist_list, response = _get_playlists(headers, username)
    playlist_id = ""
    # If the name is not in the list we post a request to create it 
    if playlist_name not in playlist_list:
        response = requests.post(
            f"https://api.spotify.com/v1/users/{username}/playlists",
            headers=headers,
            json={"name": playlist_name, "description": "", "public": False},
            timeout=5,
        )
        playlist_id = response.json().get("id")
    # else we check the returned items from the request to get the id to it
    else:
        for pl in response.json().get("items"):
            if pl.get("name") == playlist_name:
                playlist_id = pl.get("id")

    return playlist_id


def save_data_to_playlist(playlist_size, playlist_id, headers):
    """Saves data to the spotify playlist

    Parameters
    ----------
    playlist_size : int
        The number of items we get from our history
    playlist_id : str
        The id of the playlist we are generating for
    headers : dict
        Headers variable containing the token for authorization
    """

    # Read the json file to a dataframe
    df = pd.read_json("data/final_file/count_data.json", orient="split")
    # Get the number of rows we specified
    df = df.sample(n=playlist_size, weights=df.cnt)

    # Create an empty list to store the uri-s of the songs we want to add to our playlist
    uri_list = []

    # Iterate through the dataframe
    for index, row in df.iterrows():
        track = str(row["track_name"])
        artist = str(row["artist_name"])
        count = str(row["cnt"])
        uri = str(row["spotify_track_uri"])

        logger.info(
            'inserted: "%(artist)s - %(track)s" with count %(count)s'
            % {"track": str(track), "artist": str(artist), "count": str(count)}
        )

        # Add the uri to the list
        uri_list.append(uri)

    json_data = {
        "uris": uri_list,
        "position": 0,
    }

    # Post a request to add the songs to our playlist
    response = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json=json_data,
        timeout=5,
    )
