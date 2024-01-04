# Imports
import requests
import variabile_globale as vg
from get_access_token import get_access_token

def get_user_id(username):

    if username[0] == '@':
        username = username[1:]

    url = 'https://api.twitch.tv/helix/users'
    params = {'login': username}

    headers = {
        'Authorization': f"Bearer {vg.bot_access_token}",
        'Client-ID': vg.bot_client_id
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200 and len(response.json()["data"]) > 0:
        # Cerere realizată cu succes
        response_json = response.json()
        # Procesează la nevoie response JSON
        return response_json["data"][0]["id"]
    elif response.status_code == 200 and len(response.json()["data"]) == 0:
        # Cerere realizată cu succes, dar userul nu a fost găsit
        print(f"User {username} not found")
    else:
        # Cererea a eșuat
        print(f"API request failed with status code {response.status_code}: {response.text}")
        vg.bot_access_token = get_access_token()
        return get_user_id(username)