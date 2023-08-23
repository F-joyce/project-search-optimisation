import os
import subprocess
import sys
import time
import numpy as np

from numpy import savetxt
from deap.algorithms import tools, varAnd
from threading import Thread

from dict_utils import save_dictionary_data, load_dictionary_data, get_fitness, add_to_dictionary, add_to_dictionary_from_list

#from ansys.mapdl import core as pymapdl #probably the proprietary simulator
#new_path = '/home/ansys/ansys_inc/v201/ansys/bin/ansys201'
#pymapdl.change_default_ansys_path(new_path)

# TODO Function to get the dataframe
# TODO Function to check the dataframe

# calculate the fitness of a full population, gets in a population, return a list object with all the fitnesses

dictionary = load_dictionary_data('updated_dictionary.pickle')

def cal_pop_fitness(pop):

    path = os.getcwd()  # works where the script is run from

    fitness = []  # empty list for fitnesses
    loopar = 0  # counter for creating the folder and launching the simulator that will be used by supernova.py
    # iterate through the individuals in the population, update counter, save csv file with the BarrierShape, simulate(?) the barrier fitness with supernova2M.py
    for Bshape in pop:
        # shutil.rmtree(path+'/'+str(loopar), ignore_errors=True)
        # os.mkdir(path+'/'+str(loopar))
        print(loopar)
        # this creates(probably?) and change the directory to one corresponding to the counter number reached, the # of folder created at the end of the for loop should be the same as the # of individual
        os.chdir(path+'/'+str(loopar))
        # shutil.copyfile(path+'/supernova.py', path+'/'+str(loopar)+'/supernova.py')
        # save this Bshape(an array) in a csv formatted file called data.csv
        savetxt('data.csv', Bshape, delimiter=',')
        # for each Bshape in the population pop it opens a pid exectuing the script supernova2M.py, probably this load the data.csv file just created
        pid = subprocess.Popen([sys.executable, "supernova.py"])
        print("After subprocess.Popen for loop number %d" %loopar)
        loopar += 1  # updates the counter

    loopar = 0  # reset the counter to iterate through all the folders

    for Bshape in pop:  # iterate through all the folders just created to save the fitness found in the min.txt files in the list fitness
        # check the file exist, waits until it does, this file is most likely an output of the supernova2M.py script
        while not os.path.exists(path+'/'+str(loopar)+'/min.txt'):
            print(path+'/'+str(loopar)+'/min.txt')
            time.sleep(5)
        # open this min.txt and save the data in the first line to the list object "fitness"
        
        fitness_value = ""
        while type(fitness_value) == str:
            with open(path+'/'+str(loopar)+'/min.txt', 'r') as f:
                try:
                    fitness_value = float(f.readline().rstrip())
                    # Fitness in Deap needs to be stored in a tuple object
                    fitness.append(fitness_value)
                    print("Appended fitness value at %d" %loopar)
                except ValueError:
                    f.close()
            


            # add_new_fitness(Bshape) # this function updates the dataframe of fitnesses with new fitness

            time.sleep(1)  # probably to avoid issues ?
        os.remove(path+'/'+str(loopar)+'/min.txt')  # delete the min.txt file
        os.remove(path+'/'+str(loopar)+'/data.csv')  # delete the data.csv file
        loopar += 1
    os.chdir(path)
    return fitness

def batch_fitness_simulation(population, max_batch):
    initial_population = population.copy()
    total_fitnesses = []
    to_batch_up = []
    new_dictionary = {}
    for individual in population:
        if get_fitness(dictionary, individual) == False:
            to_batch_up.append(individual)
    new_fitnesses = []
    new_fitnesses_individuals = to_batch_up.copy()
    loopar = 0
    while len(to_batch_up) > 0:
        print("In the full line of individual there are still %d to process" % len(to_batch_up))
        temp_list = []
        while (len(temp_list) < max_batch) and (len(to_batch_up) > 0):
            print("In the cabin there are %d individuals" % len(temp_list))
            temp_list.append(to_batch_up.pop(0))
        fitnesses_to_append = cal_pop_fitness(temp_list)
        #loopar += len(fitnesses_to_append) #to delete if all works
        for fitness_value in fitnesses_to_append:
            new_fitnesses.append(fitness_value)
        print("In the cave there are %d workers working" % len(new_fitnesses))

    print("The new fitnesses put in a list are: ", len(new_fitnesses))
    print("The individual in the simulated list: ", len(to_batch_up) )

    new_dictionary = add_to_dictionary_from_list(dictionary, to_batch_up, new_fitnesses)
    if len(new_dictionary) == 0:
        new_dictionary = add_to_dictionary_from_list(dictionary, new_fitnesses_individuals, new_fitnesses)
    else:
        new_dictionary = add_to_dictionary_from_list(new_dictionary, new_fitnesses_individuals, new_fitnesses)
    
    save = Thread(target=save_dictionary_data, args=(new_dictionary, "dictionary.pickle"))
    print("SAVING DICTIONARY")
    save.start()
    save.join()
    print("SAVING COMPLETED")

    for individual in initial_population:
        fitness = get_fitness(dictionary, individual)
        total_fitnesses.append((fitness,))

    return total_fitnesses

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
    
    fitnesses = batch_fitness_simulation(invalid_ind, max_batch)

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
        fitnesses = batch_fitness_simulation(invalid_ind, max_batch)
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
