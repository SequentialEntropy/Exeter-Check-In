from datetime import datetime, timezone
import urllib.error
import argparse

from id_token import get_token, read_last_modified_config, read_from_config
from events import get_events
from check_in import do_check_in

def main(client_id_path="client_id.txt", refresh_token_path="refresh_token.txt") -> None:
    # Parse command-line flags
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Run in manual mode"
    )
    args = parser.parse_args()

    # Last modified date of refresh token
    last_modified = read_last_modified_config(refresh_token_path)
    print()
    print(f"Last modified time for {refresh_token_path}:")
    print(last_modified)

    # Fetch ID token
    try:
        id_token = get_token(
            client_id=read_from_config(client_id_path),
            refresh_token=read_from_config(refresh_token_path)
        )
    except urllib.error.HTTPError as e:
        print(f"Unexpected error: {e.reason}")
        print(f"Status code: {e.status}")
        print()
        print("An error occured whilst trying to fetch the id_token.")
        print("Try deleting refresh_token.txt and copy it from the browser again.")
        print()
        return

    # Fetch events
    events = get_events(id_token)
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now().astimezone()

    # Choose event
    if args.manual:
        print()
        print("Which event do you want to check in to?")
        for (i, event) in enumerate(events):
            print(f"[{i}] - {event.description}")
        i = int(input("Your selection: "))
        print()

        event = events[i]
    else:
        events = [event for event in events if event.start < now_utc < event.end]

        print()
        print(f"Unix timestamp (local): {now_local.timestamp()}")
        print(f"Unix timestamp (utc):   {now_utc.timestamp()}")
        print(f"System time (local):    {now_local}")
        print(f"System time (utc):      {now_utc}")
        print()

        if len(events) == 0:
            print("There are no events to check in to.")
            print()
            return
        event = events[0]

    # Check in to event
    print(f"Checking in to {event.description}...")
    print()
    print(f"Start time:   {event.start}")
    print(f"Current time: {now_utc}")
    print(f"End time:     {event.end}")
    print()
    print(f"Room:         {event.locations[0]['room']}")
    print()
    print(f"Latitude:     {event.get_latitude()}")
    print(f"Longitude:    {event.get_longitude()}")
    print()

    data, status_code = do_check_in(id_token, event)

    if status_code != 201:
        print(f"Unexpected error: {status_code}")
        print(data.get("error", {}).get("message", "No error message given."))
        print()
        return

    print(data)
    print()

if __name__ == "__main__":
    main()
