import random
import math
import numpy as np
import cv2 
import Hsvcolors
import BlobDetector

class GeneticAlgorithm:
    
    
    def __init__(self, image):
 
        self.image = image      

        #shape parameters
        self.SHAPECOUNT = BlobDetector.detectContours(image) #20
        print "count ", self.SHAPECOUNT

        #genetic algorithm parameters
        self.POPULATIONSIZE = 50
        self.GENERATIONS = 1000
        self.PARAMS = 4
        self.SELECTIONPROB = 0.2
        self.MUTATIONPROB = 0.1
        self.MUTATIONAMOUNT = 0.3
        #self.colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

        hsvcolors = Hsvcolors.Hsvcolors()
        self.colors = hsvcolors.getColorlists(self.image, 5)

        #get size of images
        height, width = image.shape[:2]
        self.height = height
        self.width = width
        self.diameter = math.floor(math.sqrt(height*height + width*width)/2) 

    def init_population(self):

        population = []
        for i in range(self.POPULATIONSIZE):
            individual = []
            for j in range(self.SHAPECOUNT):
                centerx = random.randint(1, self.height)  
                centery = random.randint(1, self.width)  
                radius = random.randint(1, self.diameter)  
                colorindex = random.randint(0, len(self.colors) -1)
                individual.append(centerx)
                individual.append(centery)
                individual.append(radius)
                individual.append(colorindex)

            population.append(individual)
        return population


    def calculate_fitness(self, population):
        fitness = []   
        for j in range(len(population)):
            individual = population[j]
            fitness2 = self.calculate_fitness_individual(individual)
            fitness.append(fitness2)
        return fitness

    def calculate_fitness_individual(self, individual):
        #calculate the pixel difference between the resultant image and the real image
     
        pixels = self.height * self.width
        maxfitness = 256

        img = self.draw_circles(individual)
        subtract = cv2.absdiff(self.image, img) 
        fitness1 = cv2.sumElems(subtract)
        #print fitness1
        fitness2 = fitness1[0] + fitness1[1] + fitness1[2]
        error = fitness2/pixels
        fitness2 = maxfitness - error
        
        return fitness2


    def draw_circles(self, individual):
        # Create a white image
        
        img = 255 * np.ones((self.height,self.width,3), np.uint8)
           
        for i in range(self.SHAPECOUNT):
            start = (i) * self.PARAMS
            #print start
            
            cv2.circle(img, (individual[start + 0],individual[start + 1]), individual[start + 2], self.colors[individual[start + 3]], thickness=-1, lineType=8, shift=0) 
        
        return img


    def create_roulette(self, population, fitness):
        #construct roulette wheel
        roulette = []
        total = 0
        for i in range(len(fitness)):
            total = total + fitness[i] 
            roulette.append(total)
        return roulette

    def select_individuals(self, population, roulette):
        random.randint(0, 255)  
        total = math.floor(roulette[len(roulette) - 1])  

        parent1index = random.randint(1, total)
        parent2index = random.randint(1, total) 
        while parent1index == parent2index:
            parent2index = random.randint(1, total)
        
        parent1 = 0
        while roulette[parent1] < parent1index:
            parent1 +=1 
        parent2 = 0
        while roulette[parent2] < parent1index:
            parent2+= 1

        return [parent1, parent2]


    def crossover(self, population, parent1index, parent2index):
        
        parent1 = population[parent1index]
        parent2 = population[parent2index]

        #choose crossover point
        crossoverpoint = random.randint(1, self.SHAPECOUNT * self.PARAMS)
        p1start = parent1[0: crossoverpoint]
        p1end = parent1[crossoverpoint : len(parent1)] 
        p2start = parent2[0: crossoverpoint]
        p2end = parent2[crossoverpoint : len(parent2)] 

        child1 = p1start + p2end
        child2 = p2start + p1end
        return [child1, child2]

    def mutation(self, child):

        for i in range(self.SHAPECOUNT * self.PARAMS):
            prob = random.random()
            if prob < self.MUTATIONPROB:
                if i % self.PARAMS == 0:    
                    #centerx = random.randint(1, self.height) 
                    min1 = math.floor(child[ i] *(1 - self.MUTATIONAMOUNT))
                    max1 = math.floor(child[ i] *(1 + self.MUTATIONAMOUNT) )
                    centerx = random.randint(min1, max1) 
                    if centerx > self.height:
                        centerx = self.height
                    child[ i] = centerx
                elif i % self.PARAMS == 1:     
                    #centery = random.randint(1, self.width)
                    min1 = math.floor(child[ i] *(1 - self.MUTATIONAMOUNT))
                    max1 = math.floor(child[ i] *(1 + self.MUTATIONAMOUNT) )
                    centery = random.randint(min1 , max1) 
                    if centery > self.width:
                        centery = self.width
                    child[ i] = centery
                elif i % self.PARAMS == 2:      
                    #radius = random.randint(1, self.diameter) 
                    min1 = math.floor(child[ i] *(1 - self.MUTATIONAMOUNT))
                    max1 = math.floor(child[ i] *(1 + self.MUTATIONAMOUNT) )
                    radius = random.randint(min1 , max1) 
                    if radius > self.diameter:
                        radius = int(self.diameter)
                    child[ i] = radius 
                elif i % self.PARAMS == 3:    
                    colorindex = random.randint(0, len(self.colors) -1 )
                    child[ i] = colorindex  
        return child

           
    def replace_population(self, population, child1, child2, parent1index, parent2index):
        fitness1 = self.calculate_fitness_individual(child1)
        fitness2 = self.calculate_fitness_individual(child2)

        fitness3 = self.calculate_fitness_individual(population[parent1index])
        fitness4 = self.calculate_fitness_individual(population[parent2index])

        replacedchild = child1
        childmaxfit = fitness1
        if fitness2 > fitness1:
            replacedchild = child2
            childmaxfit = fitness2

        replaceparent = parent1index
        parentminfit = fitness3
        if fitness4 < fitness3:
            replaceparent = parent2index
            parentminfit = fitness4

        #replace if best fit is better than least fit parent
        #if childmaxfit > parentminfit:
        #   population[replaceparent] = replacedchild

        population[parent1index] = child1
        population[parent2index] = child2

        return population
