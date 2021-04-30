import requests
import json

def readAccessToken():
    with open("AccessToken.txt", "r") as f:
        return f.read()

def result(domain, extraParams):
    """
    returns a list of results from `domain` with extra params `extraParams`
    
    e.g. `domain = "countries"`, `extraParams = {"limit": 10}`
    """
    url = "http://api.aviationstack.com/v1/{0}".format(domain)
    params = { "access_key": readAccessToken() }
    params.update(extraParams)
    response = requests.get(url, params)
    return response.json()["data"]


def getCountryData():
    countryData = []
    totalCountries = 252
    stepSize = 100
    for offset in range(0, totalCountries, stepSize):
        countryData += result(
            "countries", {
                "offset": offset,
                "limit": stepSize
            }
        )
    return countryData


def getDomainData(domain, totalEntries):
    data = []
    stepSize = 100
    for offset in range(0, totalEntries, stepSize):
        data += result(
            domain, 
            {
                "offset": offset,
                "limit": stepSize
            }
        )
    return data


with open("cityData.json", "w") as f:
    f.write(str(getDomainData("cities", 500)))

with open("countryData.json", "w") as f:
    f.write(str(getDomainData("countries", 200)))