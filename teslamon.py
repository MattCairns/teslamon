import requests
import json
import time
import pickle
import yaml
from pushover import Client

def main():
    config = yaml.safe_load(open("config.yml"))
    # If you want to push to pushover put your tokens here
    client = Client(config['teslamon']['pushover']['user_key'], api_token=config['teslamon']['pushover']['api_token'])
    client.send_message('Teslamon has started', title='Teslamon')

    params = {
      "query": {
        "model": "m3",
        "condition": "new",
        # "options": {
        #   "TRIM": [
        #     "MRRWD" # SR+ I think
        #     "LRRWD",
        #     "LRAWD"
        #   ],
        # },
        "arrangeby": "Price", 
        "order": "desc",
        "market": "CA", # or US
        "language": "en",
        "super_region": "north america",
        # I set this as my nearest delivery location
        "lng": -123.0835, 
        "lat": 49.2650,
        "zip": "V5T", # First 3 letters of post code or full zip code
        "range": 200
      },
      "offset": 0,
      "count": 50,
      "outsideOffset": 0,
      "outsideSearch": "false"
    }

    cmd = 'https://www.tesla.com/en_ca/inventory/api/v1/inventory-results?query=' + json.dumps(params)

    while(True):
        res = requests.get(cmd)

        cars = json.loads(res.text)
        if cars["total_matches_found"] == 0:
            print("No matches found")
            continue

        file = "/var/teslamon/inventory.pickle"
        known_cars = set([])
        try:
            known_cars = pickle.load(open(file, "rb"))
        except (OSError, IOError) as e:
            pickle.dump(known_cars, open(file, "wb"))


        for car in cars["results"]:
            vin = car["VIN"]
            try:
                trim = car["TRIM"][0]
            except:
                trim = "null"
            try:
                paint = car["PAINT"][0]
            except:
                paint = "null"
            try:
                interior = car["INTERIOR"][0]
            except:
                interior = "null"
            try:
                wheels = car["WHEELS"][0]
            except:
                wheels = "null"
            url = "https://www.tesla.com/en_CA/m3/order/" + vin

            title = trim + ", " + paint + ", " + interior + ", " + wheels 
            msg = url

            if vin not in known_cars:
                client.send_message(msg, title=title, priority=1)

            known_cars.add(vin)

        pickle.dump(known_cars, open(file, "wb"))

        print(f"STATUS: {res.status_code}")
        time.sleep(20)


if __name__ == "__main__":
    main()
