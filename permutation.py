import random

class Permutation:
    def __init__(self, path, fitness):
        self.path = path #permutacia indexov miest ulozenych v Cities
        self.fitness = fitness #prevratena hodnota dlzky cesty (ceny)

    def inversion_mutation(self):
        numOfGenes = len(self.path)
        indexOfGene1 = random.randint(0, numOfGenes-2)
        indexOfGene2 = random.randint(indexOfGene1+1, numOfGenes-1)
        pairsToSwap = (indexOfGene2 - indexOfGene1 + 1) // 2
        while(pairsToSwap):
            self.path[indexOfGene1], self.path[indexOfGene2] = self.path[indexOfGene2], self.path[indexOfGene1]
            indexOfGene1 += 1
            indexOfGene2 -= 1
            pairsToSwap -= 1

    def swap_mutation(self):
        numOfGenes = len(self.path)
        indexOfGene1 = random.randint(0, numOfGenes-2)
        indexOfGene2 = indexOfGene1 + 1
        self.path[indexOfGene1], self.path[indexOfGene2] = self.path[indexOfGene2], self.path[indexOfGene1]

    def __eq__(self, other):
        return (self.fitness == other.fitness)

    def __lt__(self, other):
        return (self.fitness < other.fitness)

    def __gt__(self, other):
        return (self.fitness > other.fitness)