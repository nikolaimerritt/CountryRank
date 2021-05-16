import requests
import json
import datetime
from countryAndIataData import getCountryToIataOfCapital, getIataToCountryCity, getCountriesOrderedByPopln


def readAccessToken():
    """ reads access token from file """
    with open("AccessToken.txt", "r") as f:
        return f.read()


def downloadFlightData(departureIata, maxEntries=100):
    """
    returns list of flight data, that is `[flight-data-dict]`
    
    list is <= `maxEntries` in length, and `ceil(totalEntries/100)` calls are made
    """
    entriesPerCall = 100
    url = "http://api.aviationstack.com/v1/flights"
    
    flightData = []
    for offset in range(0, maxEntries, entriesPerCall):
        params = { 
            "access_key": readAccessToken(),
            "offset": maxEntries,
            "limit": entriesPerCall, 
            "dep_iata": departureIata
        }
        response = requests.get(url, params)
        flightData += response.json()["data"]
    return flightData


def countryToArrivalFlightCountFrom(depCountry, countries):
    depIata = getCountryToIataOfCapital()[depCountry]
    counts = {country: 0 for country in countries}
    iataToContryCity = getIataToCountryCity()

    for flight in downloadFlightData(depIata):
        arrivalIata = flight["arrival"]["iata"]
        if arrivalIata in iataToContryCity.keys():
            arrivalCountry = iataToContryCity[arrivalIata]["country"]
            if arrivalCountry in countries:
                counts[arrivalCountry] += 1
    
    return counts