import os
import random
import numpy as np
import pandas as pd
import shutil
import matplotlib.pyplot as plt

from initialisation import function_that_build_seed, function_that_builds_configuration
from eaSimpleCustomised import eaSimple
from customMutations import mutSwapMaterialCustom

from dict_utils import save_dictionary_data_compress
from deap import base, creator, tools
import config

#configuration variables
###PATH GLOBALS#####################################
experiment_path = config.experiment_path
###PROCESS RELATED GLOBALS##########################
MAX_BATCH = config.MAX_BATCH
###GENETIC ALGORITHM PARAMETERS#####################
POPULATION = config.POPULATION
GENERATIONS = config.GENERATIONS
CX_PROBABILITY = config.CX_PROBABILITY
MUT_PROBABILITY = config.MUT_PROBABILITY
BIT_MUT_PROBABILITY = config.BIT_MUT_PROBABILITY
TOURN_SIZE = config.TOURN_SIZE
CX_TYPE = config.CX_TYPE

parameters = config.parameters
nmaterials = config.nmaterials
shape = config.shape
percentages_ranges = config.percentages_ranges

name_conf_file = config.name_conf_file
name_result_file = config.name_result_file
name_process = config.name_process
dummy_dict_path = config.dummy_dict_path

barriers_dict = config.barriers_dict
backup_dict = config.backup_dict
evaluated = config.evaluated


def function_that_creates_folders_structure(MAX_BATCH):
    for batch_number in range(MAX_BATCH):
        shutil.rmtree(f"{experiment_path}/processes/{batch_number}", ignore_errors=True)
        os.mkdir(f"{experiment_path}/processes/{batch_number}")
        shutil.copyfile(f"{experiment_path}/{name_process}", f"{experiment_path}/processes/{batch_number}/{name_process}")


def main_function_that_run_ga(p_size = POPULATION, gen=GENERATIONS):
    pop = toolbox.population(n=p_size)
    if config.seeded:
        pop2 = toolbox.seeded_pop(n=10)
        pop[:10] = pop2[:10]

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    stats.register

    pop, log = eaSimple(MAX_BATCH,  pop, toolbox, cxpb=CX_PROBABILITY, mutpb=MUT_PROBABILITY, ngen=gen,
                                   stats=stats, halloffame=hof, verbose=False)

    return pop, log, hof


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
    
    initial_main_dict_len = len(barriers_dict)
    initial_backup_len = len(backup_dict)
    initial_evaluated = len(evaluated)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("individual", function_that_builds_configuration, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("seeded_ind", function_that_build_seed, creator.Individual)
    toolbox.register("seeded_pop", tools.initRepeat, list, toolbox.seeded_ind)

    toolbox.register("mate", getattr(tools, CX_TYPE))
    toolbox.register("mutate", mutSwapMaterialCustom, indpb=BIT_MUT_PROBABILITY)
    toolbox.register("select", tools.selTournament, tournsize=TOURN_SIZE)

    function_that_creates_folders_structure(MAX_BATCH)

    pop, log, hof = main_function_that_run_ga(p_size = POPULATION, gen = GENERATIONS)

    shutil.copyfile(dummy_dict_path, f"{experiment_path}/backup/last_working_dummy.gzip")
    save_dictionary_data_compress(barriers_dict, dummy_dict_path)

    gen = log.select('gen')
    max_fitness = log.select('max')

    plt.plot(gen, max_fitness)
    plt.savefig()

    df_log = pd.DataFrame(log)

    df_log.to_csv("barriers_ga_statistics.csv", index = False)

    #print(f"Initial length: main dict {initial_main_dict_len}, backup {initial_backup_len}, eval list {initial_evaluated}")
    #print(f"Final length: main dict {len(config.barriers_dict)}, backup {len(config.backup_dict)}, eval list {len(config.evaluated)}")
    #print(f"New added to main: {len(config.barriers_dict) - initial_main_dict_len}")
