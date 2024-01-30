import requests

URL = "https://api.exeter.ac.uk/spaces/all"

def send_request(token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': '*/*',
        'Accept-Language': 'en',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://m.exeter.ac.uk/',
        'tenant': 'exeter-uk',
        'Origin': 'https://m.exeter.ac.uk',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Authorization': token,
        'Connection': 'keep-alive',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    return requests.get(
        url=URL,
        headers=headers,
        verify=False
    )

def get_buildings(token):
    data = send_request(token)

    rooms = data.json()["spaces"]

    buildings = {}
    
    for room in rooms:
        building = room.get("ancestorDetails").get("building").get("name")

        if building not in buildings:
            buildings[building] = {}

        buildings[building][room["name"]] = {
            "id": room.get("id"),
            "coordinates": room.get("location", {}).get("coordinates")
        }

    return buildings