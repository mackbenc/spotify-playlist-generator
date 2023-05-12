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
    counter = 0
    uri_list = []
    for index, row in df.iterrows():
        track = str(row["trackName"]).replace(" ", "%20")
        artist = str(row["artistName"]).replace(" ", "%20")
        search_string = f"remaster%2520track:+{track}%2520artist:+{artist}"

        response = requests.get(
            f"https://api.spotify.com/v1/search?q={search_string}&type=track&market=HU&limit=1",
            headers=headers,
            timeout=5,
        )

        items = response.json().get("tracks").get("items")
        if len(items):
            track = row["artistName"], row["trackName"]
            # print(items[0].get("external_urls").get("spotify"))
            # print(items[0].get("uri"))

            response = requests.get(
                f'https://api.spotify.com/v1/tracks/{items[0].get("id")}?market=HU',
                headers=headers,
                timeout=5,
            )

            track_back = response.json().get("artists")[0].get(
                "name"
            ), response.json().get("name")

            if track[0] != track_back[0] or (
                track_back[1] not in track[1] and track[1] not in track_back[1]
            ):
                logger.error(
                    "%(track_back)s instead of: %(track)s"
                    % {"track_back": str(track_back), "track": str(track)}
                )
                counter += 1
                continue

            if track != track_back:
                logger.info(
                    "%(track_back)s instead of: %(track)s"
                    % {"track_back": str(track_back), "track": str(track)}
                )
            else:
                logger.info("inserted: %(track)s" % {"track": str(track)})

            uri_list.append(items[0].get("uri"))

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

    return counter
