import os
import subprocess
import sys
import time
import numpy as np

from numpy import savetxt
from deap.algorithms import tools, varAnd
from threading import Thread

from dict_utils import save_dictionary_data, load_dictionary_data, get_fitness, add_to_dictionary, add_to_dictionary_from_list

####################
HEIGHT_OF_PLATE = 10
WIDTH_OF_PLATE = 50
####################

try:    
    bullets_dictionary = load_dictionary_data('bullets_dictionary.pickle')
except FileNotFoundError:
    bullets_dictionary = {}


def reshape_plates_arrays_pop(pop_plate_1d,
                              height_points=HEIGHT_OF_PLATE,
                              width_points=WIDTH_OF_PLATE):
    pop_plate_1d = np.array(pop_plate_1d)
    size = pop_plate_1d.shape[0]
    pop_plate_2d = pop_plate_1d.reshape(size,height_points,width_points)
    return pop_plate_2d

def cal_pop_fitness(pop):
    pop=reshape_plates_arrays_pop(pop)
    root_path = os.path.dirname(os.path.abspath(__file__))

    def path_to_files(x):
        n = str(x)
        s = root_path + "/file_" + n
        return s
      
    command = "python"
    script = root_path + "/solve_1.py"
    fitness = []  
    loopar = 0
    processes_started = []
    for plate_config in pop:
        print(loopar)
        os.chdir(path_to_files(loopar))
        savetxt('init_state.txt', plate_config, fmt='%.0f')
        processes_started.append(
            subprocess.Popen([command, script,str(loopar)]))
        print("Process started with file_%d" %loopar)
        loopar += 1  # updates the counter

    loopar = 0  # reset the counter to iterate through all the folders

    for plate_config in pop:  
        while not os.path.exists(path_to_files(loopar)+'/velocity.txt'):
            print(path_to_files(loopar) + '/velocity.txt')
            time.sleep(5)
        
        fitness_value = ""
        while type(fitness_value) == str:
            with open(path_to_files(loopar) + '/velocity.txt', 'r') as f:
                try:
                    line=f.readline().strip()
                    if line!='':
                        fitness_value = ((-1)*float(line)) #unused bias
                        processes_started[loopar].kill()
                    fitness.append(fitness_value)
                    print("Appended fitness value of file_%d" %loopar)
                except ValueError:
                    f.close()

            time.sleep(1)
        os.remove(path_to_files(loopar) +'/velocity.txt')
        os.remove(path_to_files(loopar) + '/init_state.txt')
        loopar += 1
    os.chdir(root_path)
    return fitness

def batch_fitness_simulation(population, max_batch):
    initial_population = population.copy()
    total_fitnesses = []
    to_batch_up = []
    new_dictionary = {}
    for individual in population:
        if get_fitness(bullets_dictionary, individual) == False:
            to_batch_up.append(individual)
    new_fitnesses = []
    new_fitnesses_individuals = to_batch_up.copy()
    #loopar = 0
    while len(to_batch_up) > 0:
        print("In the generation %d individual are due to process" % len(to_batch_up))
        temp_list = []
        while (len(temp_list) < max_batch) and (len(to_batch_up) > 0):
            temp_list.append(to_batch_up.pop(0))
        print("In the current batch for parallel processing there are %d individuals" % len(temp_list))
        fitnesses_to_append = cal_pop_fitness(temp_list)
        for fitness_value in fitnesses_to_append:
            new_fitnesses.append(fitness_value)
        print("%d new fitness value have been processed" % len(new_fitnesses))

    print("The new fitnesses put in a list are:", len(new_fitnesses))
    print("The plates processed by the simulator are:", len(to_batch_up) )

    new_dictionary = add_to_dictionary_from_list(bullets_dictionary, to_batch_up, new_fitnesses)
    if len(new_dictionary) == 0:
        new_dictionary = add_to_dictionary_from_list(bullets_dictionary, new_fitnesses_individuals, new_fitnesses)
    else:
        new_dictionary = add_to_dictionary_from_list(new_dictionary, new_fitnesses_individuals, new_fitnesses)
    
    save = Thread(target=save_dictionary_data, args=(new_dictionary, "bullets_dictionary.pickle"))
    print("SAVING DICTIONARY")
    save.start()
    save.join()
    print("SAVING COMPLETED")

    for individual in initial_population:
        fitness = get_fitness(bullets_dictionary, individual)
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
