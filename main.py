from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict
import requests
import json
import config 
from datetime import datetime
from models import StationInfo

app = FastAPI()

# Base URLs for Deutsche Bahn's API
BASE_BOARD_DEPARTURE_URL = "https://apis.deutschebahn.com/db/apis/ris-boards/v1/public/departures"
BASE_BOARD_ARRIVAL_URL = "https://apis.deutschebahn.com/db/apis/ris-boards/v1/public/arrivals"

LUISENWEG = "694850"

@app.get("/")
def read_root():
    endpoints = {
        "/stop_places/": "Get list of stop places with their names and EVA numbers",
        "/departures/": "Get departure info for a station (query parameter: station_code)",
        "/arrivals/": "Get arrival info for a station with optional arrival_time (query parameter: station_code, arrival_time)"
    }
    # Returning directly as a dictionary (FastAPI will automatically convert it to JSON)
    return {"message": "Welcome to the Public Transport API!", "endpoints": endpoints}
    

@app.get("/stop_places/", response_model=List[StationInfo])
def get_stop_places():
    try:
        # Load the pre-generated JSON file with station codes and names
        with open('filtered_stop_places.json', 'r', encoding='utf-8') as json_file:
            stop_places_data = json.load(json_file)
        
        
        return JSONResponse(content=stop_places_data, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading stop places: {str(e)}")


@app.get("/departures/")
def get_departures(station_code: str):
    try:
    
        board_departure_url = f"{BASE_BOARD_DEPARTURE_URL}/{station_code}"

        
        departure_response = requests.get(url=board_departure_url, headers=config.headers, params=config.params)

        if departure_response.status_code == 200:
            departure_data = departure_response.json()
            return JSONResponse(content=departure_data, media_type="application/json")

        else:
            raise HTTPException(status_code=departure_response.status_code, detail="Failed to fetch departure data")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching departure data: {str(e)}")


@app.get("/arrivals/")
def get_arrivals(station_code: str, arrival_time: Optional[str] = Query(None, description="Arrival time in format YYYY-MM-DDTHH:MM:SS")):
    try:
        
        board_arrival_url = f"{BASE_BOARD_ARRIVAL_URL}/{station_code}"

        # Prepare the parameters (including arrival time if provided)
        params = config.params.copy()  # Copy base params from the config
        if arrival_time:
            try:
                # Validate the arrival time format
                datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S")
                params["time"] = arrival_time
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid time format. Use 'YYYY-MM-DDTHH:MM:SS'.")

        # Make a request to the Deutsche Bahn API
        arrival_response = requests.get(url=board_arrival_url, headers=config.headers, params=params)

        if arrival_response.status_code == 200:
            arrival_data = arrival_response.json()
            return JSONResponse(content=arrival_data, media_type="application/json")

        else:
            raise HTTPException(status_code=arrival_response.status_code, detail="Failed to fetch arrival data")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching arrival data: {str(e)}")
