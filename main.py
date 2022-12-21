import matplotlib.pyplot as plt
from timeit import default_timer as timer
import random
from permutation import Permutation
from cities import Cities
from population import Population


def generateCities(mapSize_x, mapSize_y, numOfCities):
    xCoordinates = random.sample(range(mapSize_x), numOfCities)
    yCoordinates = random.sample(range(mapSize_y), numOfCities)
    allCities = tuple(zip(xCoordinates, yCoordinates)) #nahodne vygenerovane suradnice miest
    return allCities


def createRandomIndividuals(numOfIndividuals, numOfCities, cities):
    individuals = list() #mnozina jedincov s unikatnymi chromozomami
    randomPermutations = set() #nahodne generovane unikatne permutacie miest
    while len(randomPermutations) < numOfIndividuals: #vytvori unikatne permutacie indexov miest ulozenych v genes
        perm = random.sample(range(numOfCities), numOfCities) #preusporiadane indexy miest v genes
        randomPermutations.add(tuple(perm)) #tuple, lebo do setu sa daju pridat iba hashovatelne objekty
    while len(individuals) < numOfIndividuals: 
        permutation = list(randomPermutations.pop())
        individuals.append(Permutation(permutation, cities.calculateFitness(permutation)))
    return individuals


def geneticAlgorithm(genes, selectionSize, numGenerations, numOfCities, numOfChromosomes, matingPoolSize=0, elitePoolSize=0, mutationPoolSize=0, numRandomIndividuals=0):
    progress = [] #vyvoj hodnoty fitness
    population = Population(numOfChromosomes, createRandomIndividuals(numOfChromosomes, numOfCities, genes))
    population.generation.sort(reverse=True)  #usporiada jedincov v zostupnom poradi podla hodnoty fitness
    progress.append(population.generation[0].fitness)
    initialCost = 1 / population.generation[0].fitness

    for g in range(numGenerations): #tvorba generacii

        newGeneration = list() #jedince novej generacie

        for i in range(elitePoolSize): #najlepsi jedinci postupia do dalsej generacie so svojim povodnym genotypom
            individual = population.generation[i]
            newGeneration.append(individual) 

        if numRandomIndividuals != 0:
            randomPool = createRandomIndividuals(numRandomIndividuals, numOfCities, genes)
            for newInd in range(numRandomIndividuals):
                newGeneration.append(randomPool[newInd])

        matingPool = list() #zoznam rodicovskych parov
        childrenRequired = numOfChromosomes - elitePoolSize - numRandomIndividuals
        if(matingPoolSize == 0):
            matingPoolSize = childrenRequired
            if matingPoolSize % 2 == 1:
                matingPoolSize += 1
            matingPoolSize /= 2
 
        while(len(matingPool) < matingPoolSize):
            if(selectionSize == 0):
                matingPool.append(tuple(population.rouletteWheelSelection(2))) #indexy dvoch jedincov, ktore sa budu krizit
            else:
                matingPool.append(tuple(population.tournamentSelection(2, selectionSize))) 
        childrenPermutations = list() 
        childrenPermutations += population.breed(numOfCities, matingPool)

        for child_ind in range(childrenRequired):
            newGeneration.append(Permutation(childrenPermutations[child_ind], genes.calculateFitness(childrenPermutations[child_ind])))

        mutateIndividuals = list()
        while(len(mutateIndividuals) != mutationPoolSize):
            individualToMutate = random.randint(0, numOfChromosomes)
            mutateIndividuals.append(individualToMutate)

        for ind in range(mutationPoolSize):
            if(ind % 2 == 0):
                newGeneration[ind].swap_mutation()
            else:
                newGeneration[ind].inversion_mutation()

        population.newGen(newGeneration)
        population.generation.sort(reverse=True)  #usporiada jedincov v zostupnom poradi podla hodnoty fitness
        progress.append(population.generation[0].fitness)

    resultCost = 1 / population.generation[0].fitness  
    print("solution permutation: ", population.generation[0].path)
    return (initialCost, resultCost, progress)


def addDataPoints(resultsData, trialData, numGenerations):
    for i in range(numGenerations):
        resultsData[i] += trialData[i]


def initializeDataPoints(resultsData, numGenerations):
    for i in range(numGenerations):
        resultsData.append(0)


def calcAverageDataPoints(resultsData, numGenerations):
    for i in range(numGenerations):
        resultsData[i] /= numGenerations


def generateNeighbours(node, numOfCities, genes):
    indexOfRoutStartingPoint = (node.path).index(0)
    neighborhood = list()
    for indOfElement in range(numOfCities):
        if indOfElement == indexOfRoutStartingPoint:
            continue
        for newIndOfElement in range(indOfElement + 1, numOfCities):
            neighbourPath = (node.path).copy()
            if newIndOfElement == indexOfRoutStartingPoint:
                continue
            tmp = neighbourPath[newIndOfElement]
            neighbourPath[newIndOfElement] = neighbourPath[indOfElement]
            neighbourPath[indOfElement] = tmp
            neighborhood.append(Permutation(neighbourPath, genes.calculateFitness(neighbourPath)))
    neighborhood.sort(reverse=True)
    return neighborhood

def tabuSearch(sizeTabu, numGenerations, numOfCities, cities):
    progress = []
    tabuList = list()
    
    currentNode = createRandomIndividuals(1, numOfCities, cities)[0]

    initialCost = 1 / currentNode.fitness
    bestNodeYet = currentNode
    tabuList.append(currentNode)

    progress.append(currentNode.fitness)
    stop = False
    keepTurn = 0
    while not stop:
        neighborhood = generateNeighbours(currentNode, numOfCities, cities)
        bestNeighbour = neighborhood[0]

        nextBest = 1
        sizeNeighborhood = len(neighborhood)
        if(bestNeighbour.fitness < currentNode.fitness):
            if(bestNeighbour not in tabuList):
                currentNode = bestNeighbour
                tabuList.append(currentNode)
            else:
                for nextBest in range(sizeNeighborhood):
                    if(neighborhood[nextBest] not in tabuList):
                        currentNode = neighborhood[nextBest]
                        tabuList.append(currentNode)
                        break
                if nextBest == sizeNeighborhood - 1:
                    currentNode = bestNeighbour
                    tabuList.append(currentNode)
        else:
            if bestNeighbour.fitness > bestNodeYet.fitness:
                bestNodeYet = bestNeighbour
                keepTurn = 0

            currentNode = bestNeighbour
            tabuList.append(currentNode)

        if keepTurn == numGenerations:
            stop = True
        
        if len(tabuList) > sizeTabu:
            tabuList.pop(0)
      
        keepTurn += 1
        progress.append(currentNode.fitness)

    resultCost = 1 / bestNodeYet.fitness  
    print("solution permutation: ", currentNode.path)
    return (initialCost, resultCost, progress)


def main():

    nxt = 1
    while nxt:
        sizeX = input("size of the map (in x direction): ") #rozsah, z akeho vieme vyberat x-ovu suradnicu/ dlzka x-ovej osi na mape
        sizeY = input("size of the map (in y direction): ") #rozsah, z akeho vieme vyberat y-ovu suradnicu/ dlzka y-ovej osi na mape
        numOfCities = input("number of cities: ") #kolko suradnic potrebujeme
        sizeX = int(sizeX)
        sizeY = int(sizeY)
        numOfCities = int(numOfCities)
        cities = Cities(generateCities(sizeX, sizeY, numOfCities), numOfCities)
        printOutCities = input("print out generated cities? [y,n]: ")

        if printOutCities == "y":
            print(cities.allCitiesCoords)  
        
        while True:
            chosenAlgo = input("press\n'g' for genetic algorithm\n't' for tabu search\n'n' to generate new cities\n'e' to exit: ")
            if chosenAlgo == "g":
                print("define input parameters: ")
                numOfChromosomes = input("size of population: ") #kolko ciest/permutacii sa vygeneruje -> velkost populacie
                numGenerations = input("number of generations: ")
                matingPoolSize = input("mating pool size, press '0' to use default size: ") #kolko parov jedincov sa bude krizit
                elitePoolSize = input("elite pool size: ")
                numRandomIndividuals = input("number of randomly generated individuals that will appear in every generation: ")
                mutationPoolSize = input("number of times mutations will take place in every generation: ")
                selectionType = input("for roulette wheel selection press '0', for tournament selection enter the size of sample: ")
                numOfChromosomes = int(numOfChromosomes)
                numGenerations = int(numGenerations)
                matingPoolSize = int(matingPoolSize)
                elitePoolSize = int(elitePoolSize)
                numRandomIndividuals = int(numRandomIndividuals)
                mutationPoolSize = int(mutationPoolSize)
                selectionType = int(selectionType)
                t1 = timer()
                initCost, resultCost, progress = geneticAlgorithm(cities, selectionType, numGenerations, numOfCities, numOfChromosomes, matingPoolSize, elitePoolSize, mutationPoolSize, numRandomIndividuals)
                t2 = timer()
                print("execution time:", (t2-t1))
                print("initial cost value: ", initCost)
                print("solution cost value: ", resultCost)
                generateGraph = input("Generate graph to show the change of fitness values among generations? [y,n]: ")
                if generateGraph == "y":
                    plt.plot(progress)
                    plt.ylabel('Fitness')
                    plt.xlabel('Generation')
                    plt.title("Fitness development for genetic algorithm")
                    plt.show()
            elif chosenAlgo == "t":
                print("define input parameters: ")
                numGenerations = input("number of generations: ")
                sizeTabu = input("size of tabu list: ")
                numGenerations = int(numGenerations)
                sizeTabu = int(sizeTabu)
                t1 = timer()
                initCost, resultCost, progress = tabuSearch(sizeTabu, numGenerations, numOfCities, cities)
                t2 = timer()
                print("execution time:", (t2-t1))
                print("initial cost value: ", initCost)
                print("solution cost value: ", resultCost)
                generateGraph = input("Generate graph to show the change of fitness values among generations? [y,n]: ")
                if generateGraph == "y":
                    plt.plot(progress)
                    plt.ylabel('Fitness')
                    plt.xlabel('Generation')
                    plt.title("Fitness development for tabu search")
                    plt.show()
            elif chosenAlgo == "n":
                break
            elif chosenAlgo == "e":
                nxt = 0
                break
            else:
                print("invalid command")
    

main()

