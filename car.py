class Car:
    def __init__(self, car_json):
        self.vin = ''
        self.trim = ''
        self.paint = ''
        self.interior = ''
        self.wheels = ''
        self.url = ''
        self.parse_json(car_json)


    def parse_json(self, car_json):
        self.vin = car_json["VIN"]
        try:
            self.trim = car_json["TRIM"][0]
        except:
            self.trim = "null"
        try:
            self.paint = car_json["PAINT"][0]
        except:
            self.paint = "null"
        try:
            self.interior = car_json["INTERIOR"][0]
        except:
            self.interior = "null"
        try:
            self.wheels = car_json["WHEELS"][0]
        except:
            self.wheels = "null"
        self.url = "https://www.tesla.com/en_CA/m3/order/" + self.vin
