import json
import os
from datetime import datetime, timezone
try:
    import readline
except ImportError:
    pass

import fetch

script_dir = os.path.dirname(__file__)
config_dir = os.path.join(os.path.dirname(script_dir), "config")
cache_dir = os.path.join(os.path.dirname(script_dir), "cache")

def get_token(client_id, refresh_token):
    url = "https://exeter-auth-prod.auth.eu-west-2.amazoncognito.com/oauth2/token"

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'referer': 'https://m.exeter.ac.uk/',
        'origin': 'https://m.exeter.ac.uk',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'connection': 'keep-alive',
    }

    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'refresh_token': refresh_token,
    }

    data = fetch.post(
        url=url,
        headers=headers,
        data=data
    )[0]

    os.makedirs(cache_dir, exist_ok=True)
    with open(os.path.join(cache_dir, "token.json"), "w+", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4))

    return data["id_token"]

def read_from_config(filename: str) -> str:
    filepath = os.path.join(config_dir, filename)

    os.makedirs(config_dir, exist_ok=True)
    if not os.path.isfile(filepath):
        print()
        value = input(f"Enter {filename} value: ")

        with open(filepath, "w+", encoding="utf-8") as file:
            file.write(value)

        return value

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read().split()[0]

def read_last_modified_config(filename: str):
    filepath = os.path.join(config_dir, filename)

    if os.path.exists(filepath):
        last_modified = datetime.fromtimestamp(os.path.getmtime(filepath), tz=timezone.utc)
        return last_modified