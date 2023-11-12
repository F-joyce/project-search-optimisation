import os, sys
import random
import numpy as np
import pandas as pd
import time
import subprocess
import shutil
from threading import Thread
import matplotlib.pyplot as plt
from deap.algorithms import tools, varAnd

from modules import function_that_builds_configuration_global as function_that_builds_configuration

from dict_utils import get_fitness, add_to_dictionary_from_list, save_dictionary_data_compress, load_dictionary_compressed
from deap import base, creator, tools
import config

#configuration variables
###PATH GLOBALS#####################################
experiment_path = os.getcwd()
###PROCESS RELATED GLOBALS##########################
MAX_BATCH = config.MAX_BATCH
###GENETIC ALGORITHM PARAMETERS#####################
POPULATION = config.POPULATION
GENERATIONS = 5
CX_PROBABILITY = 0.7
MUT_PROBABILITY = 0.15
BIT_MUT_PROBABILITY = 0.1
TOURN_SIZE = 3
CX_TYPE = "cxTwoPoint"

parameters = 500
nmaterials = 6
shape = (25,20)
percentages_ranges = [(80,90),(0,10),(0,10),(0,10),(0,10),(0,10)]

name_conf_file = "data.txt"
name_result_file = "min.txt"
name_process = "supernova_dry.py"
experiment_path = os.getcwd()
dummy_dict_path = f"{experiment_path}/barriers_dummy_dict.gzip"

barriers_dict = {}
barriers_dict = load_dictionary_compressed(f"{experiment_path}/barriers_dummy_dict.gzip")
backup_dict = {}
evaluated = []

def eaSimple(max_batch, population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population
    :returns: A class:`~deap.tools.Logbook` with the statistics of the
              evolution

    The algorithm takes in a population and evolves it in place using the
    :meth:`varAnd` method. It returns the optimized population and a
    :class:`~deap.tools.Logbook` with the statistics of the evolution. The
    logbook will contain the generation number, the number of evaluations for
    each generation and the statistics if a :class:`~deap.tools.Statistics` is
    given as argument. The *cxpb* and *mutpb* arguments are passed to the
    :func:`varAnd` function. The pseudocode goes as follow ::

        evaluate(population)
        for g in range(ngen):
            population = select(population, len(population))
            offspring = varAnd(population, toolbox, cxpb, mutpb)
            evaluate(offspring)
            population = offspring

    As stated in the pseudocode above, the algorithm goes as follow. First, it
    evaluates the individuals with an invalid fitness. Second, it enters the
    generational loop where the selection procedure is applied to entirely
    replace the parental population. The 1:1 replacement ratio of this
    algorithm **requires** the selection procedure to be stochastic and to
    select multiple times the same individual, for example,
    :func:`~deap.tools.selTournament` and :func:`~deap.tools.selRoulette`.
    Third, it applies the :func:`varAnd` function to produce the next
    generation population. Fourth, it evaluates the new individuals and
    compute the statistics on this population. Finally, when *ngen*
    generations are done, the algorithm returns a tuple with the final
    population and a :class:`~deap.tools.Logbook` of the evolution.

    .. note::

        Using a non-stochastic selection method will result in no selection as
        the operator selects *n* individuals from a pool of *n*.

    This function expects the :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.

    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    
    fitnesses = function_that_batches(invalid_ind, max_batch)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = function_that_batches(invalid_ind, max_batch)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook

def mutSwapMaterialCustom(individual, indpb):
    """Flip the value of the attributes of the input individual and return the
    mutant. The *individual* is expected to be a :term:`sequence` and the values of the
    attributes shall stay valid after the ``not`` operator is called on them.
    The *indpb* argument is the probability of each attribute to be
    flipped. This mutation is usually applied on boolean individuals.

    :param individual: Individual to be mutated.
    :param indpb: Independent probability for each attribute to be flipped.
    :returns: A tuple of one individual.

    This function uses the :func:`~random.random` function from the python base
    :mod:`random` module.
    """
    list_ = [x for x in range(nmaterials)]
    for i in range(len(individual)):
        for ii in range(len(individual[i])):
            if random.random() < indpb:
                temp_list = list_.copy()
                temp_list.remove(individual[i][ii])
                individual[i][ii] = random.choice(temp_list)


    return individual,

def function_that_creates_folders_structure(MAX_BATCH):
    for batch_number in range(MAX_BATCH):
        shutil.rmtree(f"{experiment_path}/processes/{batch_number}", ignore_errors=True)
        os.mkdir(f"{experiment_path}/processes/{batch_number}")
        shutil.copyfile(f"{experiment_path}/{name_process}", f"{experiment_path}/processes/{batch_number}/{name_process}")

def function_that_calculate_percentages(percentages_range):
    # example of percentages range [(10,50),(40,60),(10,50)]
    percentages = []
    for i, _range in enumerate(percentages_range):
        to_add = random.randint(_range[0],_range[1])
        percentages.append(to_add)

    if sum(percentages) != 100:
        to_adjust = (sum(percentages) - 100)//len(percentages_range)
        remainder = (sum(percentages) - 100)%len(percentages_range)
        percentages = [percent - to_adjust for percent in percentages]
        to_modify = random.randint(0,len(percentages)-1)
        percentages[to_modify] -= remainder
        for i, value in enumerate(percentages):
            if value < 0:
                percentages[i] = 0
                percentages[percentages.index(max(percentages))] += value
    else:
        pass

    percentages = [percent/100 for percent in percentages]

    return percentages

def function_that_builds_configuration_dyanmic(icls, parameters, nmaterials:int, percentages_ranges:list, shape:tuple):
    assert(len(percentages_ranges)==nmaterials), "Number of materials and percentages ranges should be the same"
    instance_percentages = function_that_calculate_percentages(percentages_ranges)
    array = np.random.choice(nmaterials, parameters, instance_percentages)
    size = array.shape[0]
    array_shaped = array.reshape(size, shape[0], shape[1])
    new_configuration = icls(array_shaped.tolist())
    return new_configuration

def function_that_builds_configuration(icls):
    assert(len(percentages_ranges)==nmaterials), "Number of materials and percentages ranges should be the same"
    instance_percentages = function_that_calculate_percentages(percentages_ranges)
    print("PERCENTAGES ARE ", instance_percentages)
    array = np.random.choice(nmaterials, parameters, p=instance_percentages)
    #assert(array.shape[0] == (shape[0]*shape[1])), "parameters number do not match shape"
    array_shaped = array.reshape(shape[0], shape[1])
    new_configuration = icls(array_shaped.tolist())
    return new_configuration

def function_that_evaluate_population(pop):
    iteration = 0
    working_dir_path = os.getcwd()
    fitness = []
    for configuration in pop:
        os.chdir(f"{working_dir_path}/processes/{iteration}")
        np.savetxt(name_conf_file, configuration, fmt='%.0f')
        # shell=True should open processes in the background, but doesn't
        process = subprocess.Popen([sys.executable, name_process], 
                                   shell=False) #TODO write in docs
        iteration += 1
    
    iteration = 0

    for configuration in pop:
        start_time = time.time()
        minutes = 0
        print(f'Waiting for simulator to output result in folder {iteration}')
        while not os.path.exists(
                        f'{working_dir_path}/processes/{iteration}/{name_result_file}'):
            if time.time()-start_time > 60:
                start_time = time.time()
                minutes += 1
                print(f'Waiting for simulator to output result in folder '
                      f'{iteration} since {minutes} minute(s)')
        
        added = False
        while not added:
            with open(f'{working_dir_path}/processes/{iteration}/{name_result_file}',
                                                             'r') as file:
                try:
                    fitness_value = float(file.readline().rstrip())
                    fitness.append(fitness_value)
                    print(f'Appended fitness value for folder {iteration}')
                    added = True
                except ValueError:
                    file.close()

            time.sleep(0.001)  # probably to avoid issues ?
        os.remove(f'{working_dir_path}/processes/{iteration}/{name_result_file}')
        os.remove(f'{working_dir_path}/processes/{iteration}/{name_conf_file}') 
        iteration += 1
    os.chdir(working_dir_path)
    return fitness

def function_that_batches(population, max_batch):
    working_dictionary = barriers_dict
    backup_dictionary = backup_dict
    len_backup_initial = len(backup_dictionary)
    evaluated_ind = evaluated
    initial_population = population.copy()
    total_fitnesses = []
    to_batch_up = []
    for individual in population:
        if get_fitness(working_dictionary, individual) == False:
            to_batch_up.append(individual)
    new_fitnesses = []
    new_fitnesses_individuals = to_batch_up.copy()
    while len(to_batch_up) > 0:
        print("There are %d unseen configuration to simulate" % len(to_batch_up))
        temp_list = []
        while (len(temp_list) < max_batch) and (len(to_batch_up) > 0):
            temp_list.append(to_batch_up.pop(0))
        fitnesses_to_append = function_that_evaluate_population(temp_list)
        for fitness_value in fitnesses_to_append:
            new_fitnesses.append(fitness_value)

    print("The new fitnesses put in a list are: ", len(new_fitnesses))
    print("The individual to be calculated were: ", len(new_fitnesses_individuals))

    working_dictionary = add_to_dictionary_from_list(working_dictionary, new_fitnesses_individuals, new_fitnesses)
    backup_dictionary = add_to_dictionary_from_list(backup_dictionary, new_fitnesses_individuals, new_fitnesses)
    if len(backup_dictionary) > len_backup_initial:
        save = Thread(target=save_dictionary_data_compress, args=(backup_dictionary, f"{experiment_path}/backup_dict.gzip"))
        print("Opened Thread to save backup dictionary")
        save.start()
        save.join()
        print(f"Dictionary saved as backup_dict.gzip with {len(backup_dictionary)} configurations")
    else:
        print("No new fitnesses to save")

    for individual in initial_population:
        if isinstance(individual, np.ndarray):
            individual = list(individual)
        if individual in evaluated:
            pass
        else:
            evaluated_ind.append(individual)
        fitness = get_fitness(working_dictionary, individual)
        total_fitnesses.append((fitness,))  # fitness is stored as a tuple
                                            # for DEAP eaSimple requirements

    return total_fitnesses

def main_function_that_run_ga(p_size = POPULATION, gen=GENERATIONS):
    pop = toolbox.population(n=p_size)
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
   
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("individual", function_that_builds_configuration, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    from test_glob import function_that_build_seed

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
    plt.show()

    df_log = pd.DataFrame(log)

    df_log.to_csv("barriers_ga_statistics.csv", index = False)

