import json 
import numpy as np
from countryAndIataData import getCountryToIataOfCapital
from prettytable import PrettyTable
from transitionMatrix import getTransitionMatrix, logMatrixAsPrettyTable

def getRanks(countries):
    trans = getTransitionMatrix(countries)
    logMatrixAsPrettyTable(trans, countries, "transition-matrix.txt")
    eigvals, eigvects = np.linalg.eig(trans)
    
    indexes = sorted(range(len(eigvals)), key = lambda i: abs(eigvals[i] - 1))
    idx = indexes[0]
    ranks = eigvects[:, idx]
    if ranks[0] < 0:
        return [-x for x in ranks]
    return list(ranks) # eigenvector with eigenvalue 1 -- is unique


def writeRanksTable(countries):
    ranks = getRanks(countries)
    countriesRanked = sorted(countries, key = lambda c: ranks[countries.index(c)], reverse=True)
    ranksSorted = sorted(ranks, reverse=True)

    ranksTable = PrettyTable()
    ranksTable.field_names = ["Country", "Rank (% time spent at country)"]
    for i in range(len(countriesRanked)):
        country = countriesRanked[i]
        rank = float(100 * ranksSorted[i])
        ranksTable.add_row([country, rank])

    with open("rank-countries.txt", "w") as f:
        f.write(str(ranksTable))


# print([c for c in countries if c not in getCountryToIataOfCapital().keys()])
# logMatrixAsPrettyTable(ranks[:, idx], countries, "ranks.txt")