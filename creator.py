import cv2
import GeneticAlgorithm

k = 10

# step 0 -load the ad/product image

# Load an color image in rgb
image = cv2.imread('image7.png')
algo = GeneticAlgorithm.GeneticAlgorithm(image)

#cv2.imshow('image',image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.imwrite('imagexxx.png', image)

# step 1 - create the population

population = algo.init_population()

# for generations till fitness achieved
for i in range(algo.GENERATIONS):

    # step 2 - do fitness evaluation
    fitness = algo.calculate_fitness(population)

    for j in range(algo.POPULATIONSIZE):
        # step 3a - selection
        roulette = algo.create_roulette(population, fitness)
        [parent1index, parent2index] = algo.select_individuals(population, roulette)

        # step 3 - do crossover
        [child1, child2] = algo.crossover(population, parent1index, parent2index)

        # step 4 - do mutation
        child1 = algo.mutation(child1)    
        child2 = algo.mutation(child2)    

        # step 5 - replace
        population = algo.replace_population(population, child1, child2, parent1index, parent2index)

    if i% k == 0:
        id1 = i / k
        #get best individual and save
        fitness = algo.calculate_fitness(population)
        maxindex = fitness.index(max(fitness))
        img = algo.draw_circles( population[maxindex])
        cv2.imwrite('videz' + `id1` + '.png', img) 
        print "saving image ", i


#make a video with these images

