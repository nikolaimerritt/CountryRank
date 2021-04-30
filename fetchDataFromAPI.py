import requests
import json
from bs4 import BeautifulSoup

def dumpJson(file, Object):
    """ dumps the json of a json-able object `Object` to a file `file"""
    content = json.dumps(Object)
    with open(file, "w") as f:
        f.write(content)


def readAccessToken():
    """ reads access token from file """
    with open("AccessToken.txt", "r") as f:
        return f.read()


def getDomainData(domain, totalEntries, extraParams = {}):
    """ 
    returns list of data from "domain" (e.g. "flights", "countries"), 
    
    with optional extra parameters (e.g. `dep_iata = XYZ`) 

    from aviationstack api. list is <= `totalEntries` in length, and `ceil(totalEntries/100)` calls are made
    """
    data = []
    entriesPerCall = 100
    url = "http://api.aviationstack.com/v1/{0}".format(domain)
    
    params = { 
        "access_key": readAccessToken(),
        "offset": totalEntries,
        "limit": entriesPerCall, 
    }
    params.update(extraParams)
    
    for offset in range(0, totalEntries, entriesPerCall):
        response = requests.get(url, params)
        data += response.json()["data"]
    return data



def getIataCodesOfCities():
    """
    scrapes website with lookup table of cities and their IATA codes

    returns `{city_name: iata_code}` dict
    """
    html = requests.get("https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm").content
    soup = BeautifulSoup(html, "html.parser")
    cityToIata = {}
    
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 3:
            cityToIata.update({cells[0].get_text(): cells[2].get_text()})
    return cityToIata


def getFlightDataFromCity(cityIataCode, numResults):
    return getDomainData("flights", numResults, extraParams={"dep_iata": cityIataCode})


def dumpStaticData():
    dumpJson(getDomainData("countries", 200))
    dumpJson("iataCodes.json", getIataCodesOfCities())