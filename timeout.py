# Imports
import requests, json
import variabile_globale as vg
from get_user_id import get_user_id

def timeout(username, duration, reason):
    if username[0] == '@':
        username = username[1:]

    url = 'https://api.twitch.tv/helix/moderation/bans'
    params = {
        'broadcaster_id': vg.owner_id,
        'moderator_id': vg.bot_id
    }
    headers = {
        'Authorization': f"Bearer {vg.bot_access_token}",
        'Client-Id': vg.bot_client_id,
        'Content-Type': 'application/json'
    }
    data = {
        'data': {
            'user_id': get_user_id(username),
            'duration': duration,
            'reason': reason
        }
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))

    if response.status_code != 200:
        print(f"API request to timeout failed with status code {response.status_code}: {response.text}")