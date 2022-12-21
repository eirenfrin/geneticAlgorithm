from math import sqrt

class Cities:
    def __init__(self, coordinatesOfCities, numOfCities):
        self.allCitiesCoords = coordinatesOfCities
        self.numOfCities = numOfCities

    def calculateDistance(self, indexOfCity_1, indexOfCity_2):
        city1 = self.allCitiesCoords[indexOfCity_1]
        city2 = self.allCitiesCoords[indexOfCity_2]
        xDifference = city1[0] - city2[0]
        yDifference = city1[1] - city2[1]
        return sqrt(pow(xDifference, 2) + pow(yDifference, 2))

    def calculateFitness(self, permutation):
        sumOfDistances = 0
        for cityIndex in range(self.numOfCities-1): #indexy od 0 do predposledneho
            indexOfCity_1 = permutation[cityIndex]
            indexOfCity_2 = permutation[cityIndex+1]
            sumOfDistances += self.calculateDistance(indexOfCity_1, indexOfCity_2)
        sumOfDistances += self.calculateDistance(0, self.numOfCities-1)
        return 1/sumOfDistances #cim je vacsie, tym lepsie


    

