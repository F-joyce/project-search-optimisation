import sys, os
root_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation'
sys.path.insert(0,root_folder)
import common
from plates import common_plates_folder

import os
import shutil
import random
import pandas as pd
import numpy
import matplotlib.pyplot as plt

from eaSimpleCustomised import eaSimple
from dict_utils import save_dictionary_data_compress
from deap import base
from deap import creator
from deap import tools

###PATH GLOBALS#####################################
experiment_path = os.getcwd()
###PROCESS RELATED GLOBALS##########################
MAX_BATCH = 5
###GENETIC ALGORITHM PARAMETERS#####################
POPULATION = 5
GENERATIONS = 2
CX_PROBABILITY = 0.75
MUT_PROBABILITY = 0.2
BIT_MUT_PROBABILITY = 0.05
TOURN_SIZE = 3
CX_TYPE = "cxTwoPoint"
###DATA PARAMETERS##################################
main_dict_path = f"{common_plates_folder}/plates_main_dict.gzip"
####################################################

def get_new_plates(icls):

    percentageEmpty = random.randint(0, 50)/100
    percentageFull = 1-percentageEmpty
    array = numpy.random.choice(2, 500,p=[percentageFull, percentageEmpty])
    array[450:455] = [1,1,1,1,1]
    new_plate = icls(array.tolist())
    return new_plate


def main(p_size = POPULATION, gen=GENERATIONS):

    pop = toolbox.population(n=p_size)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    stats.register

    pop, log = eaSimple(MAX_BATCH,  pop, toolbox, cxpb=CX_PROBABILITY, mutpb=MUT_PROBABILITY, ngen=gen,
                                   stats=stats, halloffame=hof, verbose=False)

    return pop, log, hof


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("individual", get_new_plates, creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", getattr(tools, CX_TYPE))
toolbox.register("mutate", tools.mutFlipBit, indpb=BIT_MUT_PROBABILITY)
toolbox.register("select", tools.selTournament, tournsize=TOURN_SIZE)

#shutil.copyfile(main_dict_path, working_dict_path)

for batch_number in range(MAX_BATCH):
		shutil.rmtree(f"{experiment_path}/file_{batch_number}", ignore_errors=True)
		os.mkdir(f"{experiment_path}/file_{batch_number}")
	

pop, log, hof = main(p_size = POPULATION, gen = GENERATIONS)

from plates import plates_dict, backup_dict, evaluated

shutil.copyfile(main_dict_path, f"{common_plates_folder}/backup/last_working_main.gzip")
save_dictionary_data_compress(plates_dict, main_dict_path)

print(f"Added {len(backup_dict)} new configurations/fitness pair to dictionary")

gen = log.select('gen')
best_fitness = log.select('min')

plt.plot(gen, best_fitness)
plt.show()

df_log = pd.DataFrame(log)

df_log.to_csv("plates_ga_statistics.csv", index = False)
with open('total-num-eval.txt', 'w') as f:
  f.write('%d' % len(evaluated))

