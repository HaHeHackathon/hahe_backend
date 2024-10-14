import requests
import config
import json
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum
import yaml


LUISENWEG = "694850"
BOARD_DEPARTURE_URL = f"https://apis.deutschebahn.com/db/apis/ris-boards/v1/public/departures/{LUISENWEG}"
departure_response = requests.get(url=BOARD_DEPARTURE_URL, headers=config.headers, params=config.params)

if departure_response.status_code == 200:
    departure_data = departure_response.json()
    with open('departure_info.json', 'w') as json_file:
             json.dump(departure_data, json_file, indent=4)  
else:
    print(departure_response.status_code)

# BOARD_ARRIVAL_URL = "https://apis.deutschebahn.com/db/apis/ris-boards/v1/public/arrivals/8000105"
# arrival_response = requests.get(url=BOARD_ARRIVAL_URL, headers=config.headers)

# if arrival_response.status_code == 200:
#     arrival_data = arrival_response.json()
#     print(arrival_data)


class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    roles: List[Role]




################## ARCHIVE ############################################

# STATION_URL = "https://apis.deutschebahn.com/db/apis/ris-stations/v1/batch/versions"
# station_response = requests.get(url=STATION_URL, headers=config.headers, params=config.params)
# if station_response.status_code == 200:
#     st_data = station_response.json()
    
#     with open('route_info_2.json', 'w') as json_file:
#             json.dump(st_data, json_file, indent=4)     

# else:
#      print("Failed to fetch data")


# with open('route_info.json', 'r') as json_file:
#     json_data = json.load(json_file)


# filtered_results = []

# # Loop through the 'results' key
# for result in json_data['results']:
#     if 'stopPlaces' in result:
#         for stop_place in result['stopPlaces']:
#             print(stop_place)
#             if stop_place.get("state") == 'HH':
#                 filtered_results.append(stop_place)

# with open('filtered_hamburg_info.json', 'w') as json_file:
#     json.dump(filtered_results, json_file, indent=4)
