import requests
import random

URL = "https://api.exeter.ac.uk/location/check-ins"

def send_request(token, room, r=0.0000001):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': '*/*',
        'Accept-Language': 'en',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
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

    room_lat = room["coordinates"]["latitude"]
    room_lon = room["coordinates"]["longitude"]

    json_data = {
        'spaceId': room["id"],
        'userLatitude': random.uniform(room_lat - r, room_lat + r),
        'userLongitude': random.uniform(room_lon - r, room_lon + r),
        'locationAccuracy': 10,
        'tolerance': room["coordinates"].get("tolerance"),
        'canCheckIn': True,
        'altitude': 0,
        'appVersion': 'Macintosh',
        'browserName': 'firefox',
        'platform': 'MacIntel',
    }

    return requests.post(
        url=URL,
        headers=headers,
        json=json_data,
        verify=False
    )

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{"spaceId":"9c542a13-6e39-42f0-bc90-17bba861aa12","userLatitude":50.736166505166004,"userLongitude":-3.5317450761795612,"locationAccuracy":10,"tolerance":29.4,"canCheckIn":true,"altitude":0,"appVersion":"Macintosh","browserName":"firefox","platform":"MacIntel"}'
    #response = requests.post('https://api.exeter.ac.uk/location/check-ins', headers=headers, data=data, verify=False)

def check_in(token, room):
    data = send_request(token, room)

    return data.text