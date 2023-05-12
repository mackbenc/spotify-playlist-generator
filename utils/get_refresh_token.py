
import requests
import os
import json



def get_refresh_token(client_id, client_secret, code, redirect_uri):

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {"client_id": client_id, 
            "client_secret": client_secret, 
            "grant_type": 'authorization_code',
            "code": code,
            "redirect_uri": redirect_uri},


    data = f'client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}'

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    refresh_token = response.json().get("refresh_token")
    with open("refresh_token.json", 'w') as fout:
        json_dumps_str = json.dumps({"refresh_token": refresh_token}, indent=4)

def set_refresh_token(value):
    os.environ["REFRESH_TOKEN"] = value
