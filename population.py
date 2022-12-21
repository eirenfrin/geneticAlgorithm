import random

class Population:
    def __init__(self, numOfChromosomes, generation):
        self.size = numOfChromosomes
        self.generation = generation
        
    def newGen(self, newGen):
        self.generation = newGen

    def tournamentSelection(self, numOfIndividualsRequired, sampleSize): 
        matingPoolIndices = set() #unikatne indexy jedincov
        if self.size < sampleSize or self.size < numOfIndividualsRequired or self.size - numOfIndividualsRequired + 1 < sampleSize:
            print("sample size is bigger than number of individuals in population")
            return
        indiciesOfChromosomes = list(range(self.size)) #indexy vsetkych chromozomov v generacii
        while len(matingPoolIndices) < numOfIndividualsRequired: #kym nevyberieme pozadovany pocet jedincov
            tournamentBetweenChromosomes = random.sample(indiciesOfChromosomes, sampleSize) #nahodne vyberieme sampleSize jedincov z populacie
            indexOfTheFittest = tournamentBetweenChromosomes[0] #index najlepsieho jedinca vo vybranej vzorke
            fitnessOfTheFittest = self.generation[indexOfTheFittest].fitness # hodnota fitness najlepsieho jedinca vo vybranej vzorke
            for i in range(1, sampleSize):
                indexOfPotentialWinner = tournamentBetweenChromosomes[i]
                if self.generation[indexOfPotentialWinner].fitness > fitnessOfTheFittest:
                    fitnessOfTheFittest = self.generation[indexOfPotentialWinner].fitness
                    indexOfTheFittest = indexOfPotentialWinner
            matingPoolIndices.add(indexOfTheFittest)
            indiciesOfChromosomes.remove(indexOfTheFittest)
        return matingPoolIndices

    def determineIntervalsOfSelectionProbability(self):
        sumOfFitness = 0 #sucet hodnot fitness vsetkych jedincov
        for chrom in range(self.size):
            sumOfFitness += self.generation[chrom].fitness
        intervalsOfSelectionProbability = []
        upperBorderOfTheInterval = 0
        for chromosomeIndex in range(self.size - 1): #posledna je vzdy 1
            newSelectionProbability = self.generation[chromosomeIndex].fitness / sumOfFitness #velkost intervalu
            upperBorderOfTheInterval += newSelectionProbability
            intervalsOfSelectionProbability.append(upperBorderOfTheInterval)
        intervalsOfSelectionProbability.append(1)
        return intervalsOfSelectionProbability

    def rouletteWheelSelection(self, numOfIndividualsRequired):
        if numOfIndividualsRequired > self.size:
            print("sample size is bigger than number of individuals in population")
            return
        matingPoolIndices = set() #unikatne indexy jedincov
        upperBoundsOfIntervalsOfSelectionProbability = self.determineIntervalsOfSelectionProbability() 
        
        while len(matingPoolIndices) < numOfIndividualsRequired: #kym nevyberieme pozadovany pocet jedincov
            randomNumber = random.random() #cislo z intervalu [0,1)
            parentIndex = 0
            while randomNumber >= upperBoundsOfIntervalsOfSelectionProbability[parentIndex]:
                parentIndex += 1
            matingPoolIndices.add(parentIndex)
            #print("po roulette")
        return matingPoolIndices

    def crossover(self, numOfGenes, indParent1, indParent2):
        minNumOfGenesPassedFromParent = 0.3
        #child will receive at least 30% of genes from each parent
        minSizeOfSequence = int(numOfGenes * minNumOfGenesPassedFromParent) #najmesi pocet genov sekvencii, ktora sa prenesie na potomka
        maxSizeOfSequence = numOfGenes - minSizeOfSequence
        maxIndexOfGene1 = numOfGenes - minSizeOfSequence
        indexOfGene1 = random.randint(0, maxIndexOfGene1)
        minIndexOfGene2 = indexOfGene1 + minSizeOfSequence - 1     
        maxIndexOfGene2 = indexOfGene1 + maxSizeOfSequence - 1
        if(maxIndexOfGene2 > numOfGenes - 1):
            maxIndexOfGene2 = numOfGenes - 1
        indexOfGene2 = random.randint(minIndexOfGene2, maxIndexOfGene2)

        childWithSeqFromP_1 = []
        childWithSeqFromP_2 = []
        seqFromP_1 = []
        seqFromP_2 = []

        for gene in range(indexOfGene1, indexOfGene2+1):
            seqFromP_1.append(self.generation[indParent1].path[gene])
            seqFromP_2.append(self.generation[indParent2].path[gene])

        genesLeftFromP_1 = []
        genesLeftFromP_2 = []

        for gene in range(numOfGenes):
            geneFromP_1 = self.generation[indParent1].path[gene]
            geneFromP_2 = self.generation[indParent2].path[gene]
            if(geneFromP_1 not in seqFromP_2):
                genesLeftFromP_1.append(geneFromP_1)
            if(geneFromP_2 not in seqFromP_1):
                genesLeftFromP_2.append(geneFromP_2)

        gene = 0
        while gene < numOfGenes:
            if gene == indexOfGene1:
                childWithSeqFromP_1 += seqFromP_1
                childWithSeqFromP_2 += seqFromP_2
                gene = indexOfGene2 + 1
            else:
                childWithSeqFromP_1.append(genesLeftFromP_2.pop(0))
                childWithSeqFromP_2.append(genesLeftFromP_1.pop(0))
                gene += 1

        return (childWithSeqFromP_1, childWithSeqFromP_2)

    def breed(self, numOfGenes, matingPoolIndicies):
        childrenPermutations = list() #permutacie miest pre dcersku generaciu
        numOfParentsPairs = len(matingPoolIndicies)
        for indPair in range(numOfParentsPairs):
            childrenPath_1, childrenPath_2 = self.crossover(numOfGenes, matingPoolIndicies[indPair][0], matingPoolIndicies[indPair][1])
            childrenPermutations.append(childrenPath_1)
            childrenPermutations.append(childrenPath_2)
        return childrenPermutations




    