import sys, os
common_plates_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/plates'
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_plates_folder)
sys.path.insert(0,common_folder)

import os
import shutil
import random
import pandas as pd
import numpy
import deap
import matplotlib.pyplot as plt

# import deap packages required

from eaSimpleBullets import eaSimple
from deap import base
from deap import creator
from deap import tools


####################################################
####################################################
MAX_BATCH = 40
POPULATION = 120
GENERATIONS = 100
####################################################
####################################################

def from_string_to_array(array_in_string):
    x = array_in_string.replace('\n', '')
    x = x.replace('[', '')
    x = x.replace(']', '')
    array = numpy.fromstring(x, dtype=float, sep=' ')
    return array


def get_new_plates(icls):

    percentageEmpty = random.randint(0, 50)/100
    percentageFull = 1-percentageEmpty
    array = numpy.random.choice(2, 500,p=[percentageFull, percentageEmpty])
    array[450:455] = [1,1,1,1,1]
    new_plate = icls(array.tolist())
    return new_plate

def main(p_size = POPULATION, gen=GENERATIONS):

    # choose a population size: e.g. 200
    pop = toolbox.population(n=p_size)

    # keep track of the single best solution found
    hof = tools.HallOfFame(1)

    # create a statistics object: we can log what ever statistics we want using this. We use the numpy Python library
    # to calculate the stats and label them with convenient labels
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    stats.register

    # run the algorithm: we need to tell it what parameters to use
    # cxpb = crossover probability; mutpb = mutation probability; ngen = number of iterations
    pop, log = eaSimple(MAX_BATCH,  pop, toolbox, cxpb=0.75, mutpb=0.20, ngen=gen,
                                   stats=stats, halloffame=hof, verbose=False)

    return pop, log, hof


creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
# create a toolbox
toolbox = base.Toolbox()
# Attribute generator
#an individual consists of repeated genes of type "attr_bool"  - we specify 100 genes
toolbox.register("individual", get_new_plates, creator.Individual)
#  a population consist of a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

path = os.getcwd()
for loopar in range(MAX_BATCH):
		shutil.rmtree(path+'/file_'+str(loopar), ignore_errors=True)
		os.mkdir(path+'/file_'+ str(loopar))
	

pop, log, hof = main(p_size = POPULATION, gen = GENERATIONS)

gen = log.select('gen')
max_fitness = log.select('max')

plt.plot(gen, max_fitness)
plt.show()

df_log = pd.DataFrame(log)

df_log.to_csv("deap_data_bullet.csv", index = False)


