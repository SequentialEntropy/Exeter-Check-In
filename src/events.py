from datetime import datetime, timedelta
from typing import List
import fetch
from zoneinfo import ZoneInfo

uk_tz = ZoneInfo("Europe/London")
utc_tz = ZoneInfo("UTC")

class Event:
    def __init__(self, data):
        self.start = datetime.strptime(data["start"], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=uk_tz).astimezone(utc_tz)
        self.end = datetime.strptime(data["end"], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=uk_tz).astimezone(utc_tz)
        self.module_code = data["moduleCode"]
        self.duration = data["durationInMinutes"]
        self.hosts = data["hosts"]
        self.locations = data["locations"]
        self.tenant = data["tenant"]
        self.attendees = data["attendees"]
        self.type = data["subType"]
        self.link = data["link"]
        self.description = data["description"]
        self.id = data["id"]
        self.can_online = data["online"]
        self.can_in_person = data["onLocation"]

    def get_latitude(self, location_index=0):
        return self.locations[location_index]["coordinates"]["latitude"]
    
    def get_longitude(self, location_index=0):
        return self.locations[location_index]["coordinates"]["longitude"]
    
    def get_tolerance(self, location_index=0):
        return self.locations[location_index]["coordinates"]["tolerance"]
    
    def get_space_id(self, location_index=0):
        return self.locations[location_index]["space_id"]
    
    @property
    def posix_start(self):
        return int(self.start.timestamp()) * 1000
    
    @property
    def posix_end(self):
        return int(self.end.timestamp()) * 1000

def get_events(id_token: str, from_date: datetime = None, to_date: datetime = None) -> List[Event]:
    # Default to current date
    if from_date is None:
        from_date = datetime.now()
    if to_date is None:
        one_day = timedelta(days=1)
        to_date = from_date + one_day

    url = "https://api.exeter.ac.uk/events"

    params = {
        'fromDate': from_date.date(),
        'toDate': to_date.date(),
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en',
        'application-id': '51011360-172a-4a83-b74a-0dccc774ba3a',
        'authorization': id_token,
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

    data, status_code = fetch.get(
        url=url,
        params=params,
        headers=headers
    )

    if status_code == 200:
        return [Event(event) for event in data["events"]]
    return None
