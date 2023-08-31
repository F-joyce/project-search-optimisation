import sys, os
root_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation'
sys.path.insert(0,root_folder)
import common
from barriers import common_barrier_folder

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
MAX_BATCH = 1
###GENETIC ALGORITHM PARAMETERS#####################
POPULATION = 2
GENERATIONS = 2
CX_PROBABILITY = 0.5
MUT_PROBABILITY = 0.1
BIT_MUT_PROBABILITY = 0.05
TOURN_SIZE = 3
CX_TYPE = "cxTwoPoint"
###INITIALISATION PARAMETERS########################
LOWEST_PERCENTAGE_SOIL = 40
HIGHEST_PERCENTAGE_SOIL = 99
###DATA PARAMETERS##################################
main_dict_path = f"{common_barrier_folder}/barriers_main_dict.gzip"

def get_new_barriers(icls):

    percentageSoil = random.randint(LOWEST_PERCENTAGE_SOIL, HIGHEST_PERCENTAGE_SOIL)/100
    percentageConcrete = 1-percentageSoil
    array = numpy.random.choice(2, 450,p=[percentageConcrete, percentageSoil])
    potential_new_barrier = icls(array.tolist())
    new_barrier = potential_new_barrier
    return new_barrier


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


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("individual", get_new_barriers, creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", getattr(tools, CX_TYPE))
toolbox.register("mutate", tools.mutFlipBit, indpb=BIT_MUT_PROBABILITY)
toolbox.register("select", tools.selTournament, tournsize=TOURN_SIZE)


for batch_number in range(MAX_BATCH):
		shutil.rmtree(f"{experiment_path}/{batch_number}", ignore_errors=True)
		os.mkdir(f"{experiment_path}/{batch_number}")
		shutil.copyfile(f"{common_barrier_folder}/supernova.py", f"{experiment_path}/{batch_number}/supernova.py")
	

pop, log, hof = main(p_size = POPULATION, gen = GENERATIONS)

from barriers import barrier_dict, backup_dict
shutil.copyfile(main_dict_path, f"{common_barrier_folder}/backup/last_working_main.gzip")
save_dictionary_data_compress(barrier_dict, main_dict_path)
print(f"Added {len(backup_dict)} new configurations/fitness pair to dictionary")

gen = log.select('gen')
best_fitness = log.select('max')

plt.plot(gen, best_fitness)
plt.show()

df_log = pd.DataFrame(log)

df_log.to_csv("barriers_ga_statistics.csv", index = False)


