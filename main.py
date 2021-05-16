from countryAndIataData import getCountriesSortedByPopln
from rankFromMatrix import writeRanksTable

countries = getCountriesSortedByPopln()[0 : 30]
writeRanksTable(countries)