import logging

import spotipy

logger = logging.getLogger(__name__)


def get_token(client_id, client_secret, redirect_uri, scopes, username, refresh_token):
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

