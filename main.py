import json
import requests
import os
import time
import sys
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define os clear command
if(sys.platform == 'win32'):
    clear = 'cls'
else :
    clear = 'clear'

# Dictionary of cites and their metaweather ID's
cities = {
  "newyork":        "2459115",
  "louisville":     "2442327",
  "losangeles":     "2442047",
  "miami":          "2450022",
  "houston":        "2424766",
  "stlouis":        "2486982",
  "denver":         "2391279",
  "portland":       "2475687"
}

# Dictionary of cites and respective pins
cityPins = {
  "louisville":     {"red":	2,  "green":	3,  "blue":	4},
  "newyork":        {"red":	17, "green":	27, "blue":	22},
  "losangeles":     {"red":	10, "green":	9,  "blue":	11},
  "miami":          {"red":	5,  "green":	6,  "blue":	13},
  "houston":        {"red":	16, "green":	20, "blue":	21},
  "stlouis":        {"red":	14, "green":	15, "blue":	18},
  "denver":         {"red":	23, "green":	24, "blue":	25},
  "portland":       {"red":	8, "green":	7, "blue":	12}
}

# Dictionary of weather abbreviatiions and their respective led colors
weather2led = {
    "sn":   "magenta",
    "sl":   "magenta",
    "h":    "red",
    "t":    "red",
    "hr":   "green",
    "lr":   "green",
    "s":    "white",
    "hc":   "white",
    "lc":   "white",
    "c":    "white"
}

class City:
    def __init__(self, name, id, weather, rp, gp, bp):
        self.name = name
        self.id = id
        self.weather = weather
        self.led = weather2led[weather]
        self.redPin = rp
        self.greenPin = gp
        self.bluePin = bp

    def toString(self):
        print("City:\t\t" + self.name)
        print("ID:\t\t" + self.id)
        print("Weather:\t" + self.weather)
        print("LED:\t\t" + self.led)
        print("rPin:\t\t" + str(self.redPin))
        print("gPin:\t\t" + str(self.greenPin))
        print("bPin:\t\t" + str(self.bluePin))
        print("\n")

url = "https://www.metaweather.com/api/location/"

def extractWeatherFromJson(json_data):
    try:
        weather = json_data["consolidated_weather"]
    except:
        weather = json_data

    weather = weather[0]
    weather = weather["weather_state_abbr"]
    return weather


def updateWeatherforCities(cityList):
    cityList.clear()
    for city in cities:
        json_data = requests.get(url + cities[city]).json()
        weather = extractWeatherFromJson(json_data)
        cityList.append(City(city, cities[city], weather, cityPins[city]["red"], cityPins[city]["green"], cityPins[city]["blue"]))


def updateWeatherforCitiesWithDate(cityList, date):
    cityList.clear()
    for city in cities:
        json_data = requests.get(url + cities[city] + date).json()
        weather = extractWeatherFromJson(json_data)
        cityList.append(City(city, cities[city], weather, cityPins[city]["red"], cityPins[city]["green"], cityPins[city]["blue"]))

def displayCities(cityList):
    try:
        while True:
            os.system(clear)
            if(len(cityList) == 0):
                print("Please update first")
            else:
                for city in cityList:
                    city.toString()
                    if(city.led == "red"):
                        light_led(city.redPin, [city.redPin, city.greenPin,  city.bluePin])
                    if(city.led == "blue"):
                        light_led(city.bluePin, [city.redPin, city.greenPin,  city.bluePin])
                    if(city.led == "green"):
                        light_led(city.greenPin, [city.redPin, city.greenPin,  city.bluePin])
                    if(city.led == "magenta"):
                        light_led_magenta([city.redPin, city.greenPin,  city.bluePin])
                    if(city.led == "white"):
                        light_led_white([city.redPin, city.greenPin,  city.bluePin])
            time.sleep(100)
    except KeyboardInterrupt:
        pass

def light_led(color, pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    GPIO.setup(color, GPIO.OUT)
    GPIO.output(color, 1)

def light_led_white(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)

def light_led_magenta(pins):
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.output(pins[0], 1)
    GPIO.setup(pins[1], GPIO.OUT)
    GPIO.output(pins[1], 0)
    GPIO.setup(pins[2], GPIO.OUT)
    GPIO.output(pins[2], 1)

def light_led_clear(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)  

def main():
    cityList = []

    choice = 0
    while(choice != '6'):
        os.system(clear)
        choice = input('(1) Update w/ current (2) Display (3) Update w/Forecast (4) Auto-update Mode (5) Clear Display (6) Exit\r\n')

        if(choice == '1'):
            print("Updating cities with current information from https://www.metaweather.com")
            updateWeatherforCities(cityList)
        elif(choice == '2'):
            displayCities(cityList)
        elif(choice == '3'):
            advance = int(input('Enter days in advance to get forecast(1-10)\r\n'))
            while(advance < 1 or advance > 10):
                advance = int(input('Enter days in advance to get forecast(1-10)\r\n'))

            forecastDate = datetime.date.today() + datetime.timedelta(days=advance)
            forecastDate = forecastDate.strftime("/%Y/%m/%d")
            print("Updating cities with forecast information from https://www.metaweather.com")
            updateWeatherforCitiesWithDate(cityList, forecastDate)
        elif(choice == '4'):
            # Update every ten minutes
            try:
                print("Auto-updating once every ten miutes")
                while True:
                    print("Updating cities with current information from https://www.metaweather.com")
                    updateWeatherforCities(cityList)
                    print("Finished updating")
                    time.sleep(1*60*10)
            except KeyboardInterrupt:
                pass
        elif(choice == '5'):
            for city in cityList:
                light_led_clear([city.redPin, city.greenPin,  city.bluePin])
        elif(choice == '6'):
            print("Exiting...")
        else:
            print("Invalid Entry...")



if __name__ == '__main__':
    main()
