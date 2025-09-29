import urllib.error
from typing import Tuple, Dict

from events import Event
import fetch

def do_check_in(id_token: str, event: Event) -> Tuple[Dict, int]:
    url = "https://api.exeter.ac.uk/location/check-ins"

    data = {
        'spaceId': event.get_space_id(),
        'userLatitude': event.get_latitude(),
        'userLongitude': event.get_longitude(),
        'locationAccuracy': 13.013,
        'tolerance': event.get_tolerance(),
        'canCheckIn': True,
        'altitude': 0,
        'appVersion': 'PlatformType.web',
        'browserName': 'native app',
        'platform': 'PlatformType.web',
        'id': event.id,
        'activityDescription': event.description,
        'startDate': event.posix_start,
        'endDate': event.posix_end,
        'moduleCode': event.module_code,
        'allDay': False,
        'type': event.type,
        'isOnline': event.can_online,
        'isOnLocation': event.can_in_person,
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en',
        'application-id': '51011360-172a-4a83-b74a-0dccc774ba3a',
        'authorization': id_token,
        'content-type': 'application/json; charset=utf-8',
        'origin': 'https://m.exeter.ac.uk',
        'priority': 'u=1, i',
        'referer': 'https://m.exeter.ac.uk/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'tenant': 'exeter-uk',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    try:
        data, status_code = fetch.post(
            url=url,
            data=data,
            headers=headers
        )
    except urllib.error.HTTPError as e:
        data, status_code = fetch.decode(e), e.getcode()

    return data, status_code
