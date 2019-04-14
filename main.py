import json
import requests
import os
import time
import sys
import datetime

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
  "stlouis":        "2486982"
}

# Dictionary of weather abbreviatiions and their respective led colors
weather2led = {
    "sn":   "blue",
    "sl":   "blue",
    "h":    "red",
    "t":    "red",
    "hr":   "green",
    "lr":   "green",
    "s":    "green",
    "hc":   "white",
    "lc":   "white",
    "c":    "white"
}

class City:
    def __init__(self, name, id, weather):
        self.name = name
        self.id = id
        self.weather = weather
        self.led = weather2led[weather]

    def toString(self):
        print("City:\t\t" + self.name)
        print("ID:\t\t" + self.id)
        print("Weather:\t" + self.weather)
        print("LED:\t\t" + self.led)
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
        cityList.append(City(city, cities[city], weather))


def updateWeatherforCitiesWithDate(cityList, date):
    cityList.clear()
    for city in cities:
        json_data = requests.get(url + cities[city] + date).json()
        weather = extractWeatherFromJson(json_data)
        cityList.append(City(city, cities[city], weather))

def displayCities(cityList):
    try:
        while True:
            os.system(clear)
            if(len(cityList) == 0):
                print("Please update first")
            else:
                for city in cityList:
                    city.toString()
            time.sleep(100)
    except KeyboardInterrupt:
        pass


def main():
    cityList = []

    choice = 0
    while(choice != '5'):
        os.system(clear)
        choice = input('(1) Update w/ current (2) Display (3) Update w/Forecast (4) Auto-update Mode (5) Exit\r\n')

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
            print("Exiting...")
        else:
            print("Invalid Entry...")



if __name__ == '__main__':
    main()
