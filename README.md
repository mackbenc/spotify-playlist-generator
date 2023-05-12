# Spotify Playlist Generator

This python based project generates/adds songs from your listening history. The songs that are added to the are random selected, but based on the number of times you listened to that song, so in the end you would get songs you listened to a lot (or few times) but may have forgotten

## Get your info
* Get your history generated from [here.](https://www.spotify.com/us/account/privacy/)

* Create an app (and add a redirect uri for it) for yourself and get your credentials from [here.](https://developer.spotify.com/dashboard)

* Get a code for your refresh-token from this link: (substitute your client_id and redirect_uri)

```https://accounts.spotify.com/authorize?response_type=code&client_id={your_client_id}&scope=playlist-modify-private&redirect_uri={your_redirect_uri}```

The code you need will be returned in your search bar like this:
```{your_redirect_uri}/callback?code={your_code}```

__important to note this code is only usable once.__
Although with the refresh token saved you don't need it anymore. If you delete the file saved you need to add the new code to the environment variables.


## Init

__Add your StreamingHistory.json files under the data/all_history path__

install python and venv

```bash
pip install venv
```
init your venv
```bash
python3 -m venv spotify-playlist-generator
```
Copy paste your credentials to the bottom of the __spotify-playlist-generator/bin/activate__ file.

```
export USERNAME=""
export CLIENT_ID=""
export CLIENT_SECRET=""
export REDIRECT_URI=""
export CODE=""
```

Activate venv

```
source spotify-playlist-generator/bin/activate
```
Install dependencies:

```
pip install -r requirements.txt
```
Run the generator:

```
python3 main.py
```

Exit the venv:

```
deactivate
```