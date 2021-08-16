import requests, json, time, pickle, yaml, logging, datetime
from car import *
from pushover import Client

def main():
    config = yaml.safe_load(open("config.yml"))
    # If you want to push to pushover put your tokens here
    client = Client(config['teslamon']['pushover']['user_key'], api_token=config['teslamon']['pushover']['api_token'])
    client.send_message('Teslamon has started.', title='Teslamon')

    file = config['teslamon']['inventory_location'] + "inventory.pickle"
    print('Teslamon has started.')
    print(f'Storing inventory at {file}')

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

    known_cars = set([])
    try:
        known_cars = pickle.load(open(file, "rb"))
    except (OSError, IOError) as e:
        pickle.dump(known_cars, open(file, "wb"))

    while(True):
        time.sleep(15)
        res = requests.get(cmd)

        inventory = json.loads(res.text)
        if inventory["total_matches_found"] == 0:
            print('No matches found in inventory')
        else:
            for c in inventory["results"]:
                car = Car(c)

                title = car.trim + ", " + car.paint + ", " + car.interior + ", " + car.wheels 

                if car.vin not in known_cars:
                    client.send_message(car.url, title=title, priority=1)
                    print(f'Found new VIN: {car.vin}')

                known_cars.add(car.vin)

            pickle.dump(known_cars, open(file, "wb"))

        now = datetime.datetime.now()
        print(f'{now}: STATUS = {res.status_code}')


if __name__ == "__main__":
    main()
