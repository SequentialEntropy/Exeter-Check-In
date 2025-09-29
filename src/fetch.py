from typing import Tuple, Union, Dict
import urllib.request
import urllib.parse
import json

def post(url: str, data: Dict, headers: Dict) -> Tuple[Union[str, Dict], int]:
    # Create urllib.request instance
    if "application/x-www-form-urlencoded" in headers["content-type"]:
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    else:
        encoded_data = json.dumps(data).encode('utf-8')
    request          = urllib.request.Request(url, data=encoded_data, headers=headers, method="POST")

    # Send request
    with urllib.request.urlopen(request) as response:
        return decode(response), response.getcode()

def get(url: str, params: Dict, headers: Dict) -> Tuple[Union[str, Dict], int]:
    # Create urllib.request instance
    url_with_params = f"{url}?{urllib.parse.urlencode(params)}"
    request         = urllib.request.Request(url_with_params, headers=headers)

    # Send request
    with urllib.request.urlopen(request) as response:
        return decode(response), response.getcode()
    
def decode(response) -> Union[str, Dict]:
    data = response.read().decode('utf-8')
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return data
