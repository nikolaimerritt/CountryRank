import json 
import numpy as np
from countryAndIataData import getRankedCountries
from prettytable import PrettyTable
from transitionMatrix import getTransitionMatrix, logMatrixAsPrettyTable

countries = getRankedCountries()[0 : 10]
trans = getTransitionMatrix(countries)

eigvals, eigvects = np.linalg.eig(trans)
idx = list(eigvals).index(1)
ranks = list(eigvects[:, idx]) # eigenvector with eigenvalue 1 -- is unique

countriesRanked = sorted(countries, key = lambda c: ranks[countries.index(c)], reverse=True)
ranksSorted = sorted(ranks, reverse=True)

ranksTable = PrettyTable()
ranksTable.field_names = ["Country", "Rank"]
for i in range(len(countriesRanked)):
    country = countriesRanked[i]
    rank = float(ranksSorted[i])
    ranksTable.add_row([country, rank])

with open("rank-countries.txt", "w") as f:
    f.write(str(ranksTable))

# logMatrixAsPrettyTable(ranks[:, idx], countries, "ranks.txt")