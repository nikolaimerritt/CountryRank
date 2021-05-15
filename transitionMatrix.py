import json 
import numpy as np
from flightData import countryToArrivalFlightCountFrom
from prettytable import PrettyTable


def logMatrixAsPrettyTable(matrix, countries, filename):
    table = PrettyTable()
    table.field_names = ["\t"] + countries
    
    for i in range(len(countries)):
        table.add_row([countries[i]] + list(matrix[i, :]))
    
    with open(filename, "w") as f:
        f.write(str(table))


def isfloat(stringy):
    try:
        float(stringy)
        return True
    except:
        return False


def readMatrixAndCountries(filename):
    matrix = []
    with open(filename, "r") as f:
        lines = f.readlines()

        countries = [x.strip() for x in lines[1].split("|") if x.strip() != ""]

        for row in lines:
            if "." in row:
                matrix.append([round(float(x), 1) for x in row.split("|") if isfloat(x)])
        return np.array(matrix), countries



def generateTransitionMatrix(countries):
    """ 
    trans[i][j] is weight that node i gives to node j 
    fetches flight data
    """
    N = len(countries)
    trans = np.zeros((N, N)) 
    
    for col in range(N):
        departure = countries[col]
        counts = countryToArrivalFlightCountFrom(departure, countries)
        counts[countries[col]] = 0
        countsArranged = np.array([counts[dest] for dest in countries])
        
        if not all(c == 0 for c in countsArranged):
            weightings = countsArranged / sum(countsArranged)
            trans[:, col] = weightings
        else:
            trans[:, col] = np.array([1/(N-1) if i != col else 0 for i in range(N) ])
    
    return trans


def getTransitionMatrix(countries):
    filename = "transition-matrix.txt"
    try:
        trans, countriesInFile = readMatrixAndCountries(filename)
        if countriesInFile == countries:
            return trans
        else:
            trans = generateTransitionMatrix(countries)
    except:
        trans = generateTransitionMatrix(countries)

# logMatrixAsPrettyTable(getTransitionMatrix(countries), countries)
# print(readMatrixAndCountries("matrix.txt"))
