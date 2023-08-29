import sys, os
common_barrier_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/barriers'
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_barrier_folder)
sys.path.insert(0,common_folder)

import shutil
import random
import pandas as pd
import numpy
import matplotlib.pyplot as plt

from eaSimpleCustomised import eaSimple
from dict_utils import dict_merger_files
from deap import base
from deap import creator
from deap import tools

###PATH GLOBALS#####################################
experiment_path = os.getcwd()
###PROCESS RELATED GLOBALS##########################
MAX_BATCH = 5
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
working_dict_path = f"{experiment_path}/storage_dictionary.gzip"


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

path = experiment_path

shutil.copyfile(main_dict_path, working_dict_path)

for batch_number in range(MAX_BATCH):
		shutil.rmtree(f"{path}/{batch_number}", ignore_errors=True)
		os.mkdir(f"{path}/{batch_number}")
		shutil.copyfile(f"{common_barrier_folder}/supernova.py", f"{path}/{batch_number}/supernova.py")
	
def run_experiments(times, function):
    
    global toolbox
    list_individuals = [] 
    list_best_values = []
    list_gens = []

    for i in range(times):
        
        pop, log, hof = function(p_size = POPULATION, gen = GENERATIONS)

        best = hof[0].fitness.values[0]   # best fitness found is stored at index 0 in the hof list

        max = log.select("max")  # max fitness per generation stored in log

        for ii in range(GENERATIONS):  # set to ngen
            fit = max[ii]
            if fit == best:
                break     

        list_individuals.append(hof[0])
        list_best_values.append(best)
        list_gens.append(ii)
        df_log = pd.DataFrame(log)
        number = str(i)
        df_log.to_csv("data_of_run_"+number+".csv", index = False)
        print("#############Cleaning Folders#############")
        #subprocess.Popen(["clean.bat"])
        #end for loop experiments


    for i in range(times):
        print(f"At iteration number {i}")
        print(f"The best individual has a fitness value of {list_best_values[i]}")

    shutil.copyfile(main_dict_path, f"{common_barrier_folder}/backup/last_working_main.gzip")
    dict_merger_files([main_dict_path,working_dict_path], main_dict_path)

    return list_individuals, list_best_values, list_gens

run_experiments(3, main)


