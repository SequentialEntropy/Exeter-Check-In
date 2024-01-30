import requests
import json

URL = "https://exeter-auth-prod.auth.eu-west-2.amazoncognito.com/oauth2/token"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Referer': 'https://m.exeter.ac.uk/',
    'Origin': 'https://m.exeter.ac.uk',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Connection': 'keep-alive',
}

def send_request(client_id, refresh_token):

    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'refresh_token': refresh_token,
    }

    return requests.post(
        url=URL,
        headers=HEADERS,
        data=data,
        verify=False,
    )

def get_token(client_id, refresh_token):
    data = send_request(client_id, refresh_token)

    with open("token_cache.json", "w+") as file:
        file.write(data.text)

    return data.json()["id_token"]

def get_token_from_cache():
    
    with open("token_cache.json", "r") as file:
        data = json.loads(file.read())

    return data["id_token"]