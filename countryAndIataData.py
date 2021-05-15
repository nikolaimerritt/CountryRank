import requests
import json
from bs4 import BeautifulSoup

def log(toLog):
    with open("log.txt", "w") as f:
        f.write(str(toLog))


def before(text, subtext):
    if subtext in text:
        return text.split(subtext)[0]
    else:
        return text


def loadJsonFileElseGenerate(filename, generateData):
    try:
        return json.load(open(filename, "r"))
    except:
        data = generateData()
        json.dump(data, open(filename, "w"))
        return data


def santisie(areaName):
    if areaName == "PR China":
        return "China"
    elif areaName == "United States":
        return "USA"
    else:
        areaName = areaName.replace(".", "")
        areaName = before(areaName, "[")
        areaName = before(areaName, " (")
        return areaName
    

def downloadCountryToCapital():
    """
    scrapes website with lookup table of countries and their capital city

    returns `{country: capital}` dict
    """
    url = "https://geographyfieldwork.com/WorldCapitalCities.htm"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    countryToCapital = {}

    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 2:
            country = santisie(cells[0].get_text())
            capital = santisie(cells[1].get_text())
            countryToCapital.update({
                country: capital
            })
    
    return countryToCapital


def getCountryToCapital():
    return loadJsonFileElseGenerate("country-to-capital.json", downloadCountryToCapital)


def downloadIataToCountryCity():
    """
    scrapes website with lookup table of IATA codes and the country of the city they correspond to

    returns `{iata: {"country": country, "city": city}}` dict
    """
    url = "https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    iataToCountryCity = {}
    
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 3:
            city = santisie(cells[0].get_text())
            country = santisie(cells[1].get_text())
            iata = cells[2].get_text()
            iataToCountryCity.update({
                iata: {
                    "country": country,
                    "city": city
                }
            })
    
    return iataToCountryCity


def getIataToCountryCity():
    return loadJsonFileElseGenerate("iata-to-country-city.json", downloadIataToCountryCity)


def generateCountryToIataOfCapital():
    countryToCapital = getCountryToCapital()
    iataToCountryCity = getIataToCountryCity()
    
    countryToIataOfCapital = {}
    
    for country in countryToCapital.keys():
        capital = countryToCapital[country]
        for iata in iataToCountryCity.keys():
            if iataToCountryCity[iata]["country"] == country:
                if capital == iataToCountryCity[iata]["city"] or capital + " " in iataToCountryCity[iata]["city"] or " " + capital in iataToCountryCity[iata]["city"]:
                    countryToIataOfCapital.update({
                        country: iata
                    })
                    break
    
    return countryToIataOfCapital


def getCountryToIataOfCapital():
    return loadJsonFileElseGenerate("country-to-iata-of-capital.json", generateCountryToIataOfCapital)


def downloadRankedCountries():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    
    countryToPopulation = {}
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 4:
            country = cells[0].a.get_text()
            population = cells[4].get_text().replace(",", "")
            countryToPopulation.update({
                country: int(population)
            })
    
    rankedCountries = countryToPopulation.keys()
    sorted(rankedCountries, key=lambda country: countryToPopulation[country])
    return countryToPopulation

def getRankedCountries():
    countryAndPopln = loadJsonFileElseGenerate("ranked-countries.json", downloadRankedCountries)
    countries = countryAndPopln.keys()
    countries = sorted(countries, key=lambda country: countryAndPopln[country], reverse=True)
    return countries

json.dump(generateCountryToIataOfCapital(), open("country-to-iata-of-capital.json", "w"))