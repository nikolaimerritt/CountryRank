import requests

def readAccessToken():
    with open("AccessToken.txt", "r") as f:
        return f.read()

def result(domain, data):
    url = "http://api.aviationstack.com/v1/{0}".format(domain)
    params = { "access_key": readAccessToken() }
    params.update(data)
    response = requests.get(url, params)
    return response.json()["data"]


def log(contents):
    with open("log.txt", "w") as logfile:
        logfile.write(str(contents))


def allCountryNames():
    names = []
    totalCountries = 252
    stepSize = 50
    for offset in range(0, totalCountries, stepSize):
        names += [data["country_name"] for data in result("countries", {
                        "offset": offset,
                        "limit": stepSize
                    }
                )]
    return names

log("\n".join(allCountryNames()))