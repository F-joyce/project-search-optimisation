import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

from threading import Thread
from dict_utils import (save_dictionary_data_compress, 
                        load_dictionary_compressed, 
                        get_fitness, add_to_dictionary_from_list)

from barriers_evaluate import evaluate_pop_fitness

cwd_path = os.getcwd()
stored_dict_name = 'storage_dictionary.gzip'

def batch_fitness_simulation(population, max_batch):
    initial_dictionary = load_dictionary_compressed(f"{cwd_path}/{stored_dict_name}")
    working_dictionary = initial_dictionary.copy()
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
        fitnesses_to_append = evaluate_pop_fitness(temp_list)
        for fitness_value in fitnesses_to_append:
            new_fitnesses.append(fitness_value)

    print("The new fitnesses put in a list are: ", len(new_fitnesses))
    print("The individual to be calculated were: ", len(new_fitnesses_individuals))

    working_dictionary = add_to_dictionary_from_list(working_dictionary, new_fitnesses_individuals, new_fitnesses)
    if len(working_dictionary) > len(initial_dictionary):
        save = Thread(target=save_dictionary_data_compress, args=(working_dictionary, f"{cwd_path}/{stored_dict_name}"))
        print("Opened Thread to save dictionary")
        save.start()
        save.join()
        print(f"Dictionary saved as {stored_dict_name}")
    else:
        print("No new fitnesses to save")

    for individual in initial_population:
        fitness = get_fitness(working_dictionary, individual)
        total_fitnesses.append((fitness,))  # fitness is stored as a tuple
                                            # for DEAP eaSimple requirements

    return total_fitnesses