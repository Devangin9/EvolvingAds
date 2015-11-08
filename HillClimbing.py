import cv2
import GeneticAlgorithm
import random


image = cv2.imread('image7.png')
algo = GeneticAlgorithm.GeneticAlgorithm(image)



individual = []
for j in range(algo.SHAPECOUNT):
    centerx = random.randint(1, algo.height)  
    centery = random.randint(1, algo.width)  
    radius = random.randint(1, algo.diameter)  
    colorindex = random.randint(0, len(algo.colors) -1)
    individual.append(centerx)
    individual.append(centery)
    individual.append(radius)
    individual.append(colorindex)



fitness = 0
i = 0
while fitness < 255:
    
    #mutate the individual
    individual2 = algo.mutation(individual)    

    #replace individual if fitness is more
    fitness2 = algo.calculate_fitness_individual( individual2)

    if fitness2 > fitness:
        individual2 = individual
        fitness = fitness2


        img = algo.draw_circles( individual)
        cv2.imwrite('videy' + `i` + '.png', img) 
        print "saving image ", i

        i = i + 1
