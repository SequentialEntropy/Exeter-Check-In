from get_token import get_token, get_token_from_cache
from get_buildings import get_buildings
from menu import select_menu, bool_menu
from check_in import check_in
import json

with open("client_id.txt", "r") as file:
    client_id = file.read()

with open("refresh_token.txt", "r") as file:
    refresh_token = file.read()

if __name__ == "__main__":
    if bool_menu("Reuse token?"):
        token = get_token_from_cache()
    else:
        print("Fetching token...")
        token = get_token(client_id, refresh_token)

    if bool_menu("Re-download buildings?"):
        print("Downloading rooms...")
        buildings = get_buildings(token)
        with open("buildings.json", "w+") as file:
            file.write(json.dumps(buildings, indent=4))
    else:
        with open("buildings.json", "r") as file:
            buildings = json.loads(file.read())

    print("Done!")

    building_name, building = select_menu(buildings, "Building")
    room_name, room = select_menu(building, f"Room ({building_name})")

    print(room["coordinates"])

    if bool_menu(f"Check in to {building_name}/{room_name}?"):
        print(check_in(token, room))
        print("Checked in!")
    else:
        print("Cancelled!")