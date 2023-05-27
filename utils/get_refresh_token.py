import json
import logging
import os

import requests
import spotipy

logger = logging.getLogger(__name__)

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
CODE = os.environ["CODE"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
SCOPES = ["playlist-modify-private"]


def _get_token(client_id, client_secret, redirect_uri, scopes, username, refresh_token) -> str:
    """Gets the token with our credentials to authenticate with

    
    Parameters
    ----------
    client_id : str
        our client id
    client_secret : str
        our client secret
    redirect_uri : str
        our redirect uri
    scopes : list
        a list containing the scopes we want to get access to
    username : str
        our username
    refresh_token : str
        our refresh token


    Returns
    -------
    str
        returns our access token
    """
    sp_oauth = spotipy.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=" ".join(scopes),
        username=username,
        show_dialog=True,
    )

    code = sp_oauth.refresh_access_token(refresh_token)

    return code.get("access_token")


def _check_refresh_token():
    """Checks if our refresh_token.json file is already generated.
    If it does not exists it generates it.

    """
    check_refresh_token_file = os.path.isfile("refresh_token.json")
    if check_refresh_token_file != True:
        logger.info("Generating refresh_token.json file")
        _get_refresh_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=CODE,
            redirect_uri=REDIRECT_URI,
        )
    else:
        logger.info("refresh_token.json file already exists. Token generating skipped")


def _get_refresh_token(client_id, client_secret, code, redirect_uri):
    """Gets the token with our credentials to authenticate with

    
    Parameters
    ----------
    client_id : str
        our client id
    client_secret : str
        our client secret
    code : str
        our code
    redirect_uri : str
        our redirect uri


    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = (
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
    )

    data = f"client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}"

    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )

    refresh_token = response.json().get("refresh_token")

    with open("refresh_token.json", "w") as :
        json_dumps_str = json.dumps({"refresh_token": refresh_token}, indent=4)
        fout.write(json_dumps_str)


def _set_refresh_token(value):
    """Sets the refresh token environment variable

    
    Parameters
    ----------
    value : str
        the refresh token value


    """
    os.environ["REFRESH_TOKEN"] = value


def get_header(username):
    """Generate a headers dict for us that contains the token to authenticate with

    
    Parameters
    ----------
    username : str
        our username


    """

    _check_refresh_token()
    refresh_token = json.load(open("refresh_token.json"))["refresh_token"]

    token = _get_token(
        username=username,
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

    return headers
