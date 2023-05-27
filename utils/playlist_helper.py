import logging

import requests

logger = logging.getLogger(__name__)


def _get_playlists(headers, username, limit=50) -> tuple:
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
    playlist_list = [pl.get("name") for pl in response.json().get("items")]
    return (playlist_list, response)


def create_or_get_playlist(headers, playlist_name, username) -> str:
    playlist_list, response = _get_playlists(headers, username)
    # If playlist exists dont create it again (you can lol)
    playlist_id = ""
    if playlist_name not in playlist_list:
        response = requests.post(
            f"https://api.spotify.com/v1/users/{username}/playlists",
            headers=headers,
            json={"name": playlist_name, "description": "", "public": False},
            timeout=5,
        )
        playlist_id = response.json().get("id")
    else:
        for pl in response.json().get("items"):
            if pl.get("name") == playlist_name:
                playlist_id = pl.get("id")

    return playlist_id


def save_data_to_playlist(df, playlist_id, headers):
    uri_list = []
    for index, row in df.iterrows():
        track = str(row["track_name"])
        artist = str(row["artist_name"])
        count = str(row["cnt"])
        uri = str(row["spotify_track_uri"])

        logger.info(
            'inserted: "%(artist)s - %(track)s" with count %(count)s'
            % {"track": str(track), "artist": str(artist), "count": str(count)}
        )
        uri_list.append(uri)

    json_data = {
        "uris": uri_list,
        "position": 0,
    }

    response = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json=json_data,
        timeout=5,
    )

    print(response.content)
