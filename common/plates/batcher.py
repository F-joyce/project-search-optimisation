import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

from threading import Thread
from dict_utils import (save_dictionary_data_compress, 
                        load_dictionary_compressed, 
                        get_fitness, add_to_dictionary_from_list)

from plates_evaluate import evaluate_pop_fitness
from GA_plates_template import plates_dict, backup_dictionary
cwd_path = os.getcwd()

def batch_fitness_simulation(population, max_batch):
    working_dictionary = plates_dict
    len_backup_initial = len(backup_dictionary)
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
    backup_dictionary = add_to_dictionary_from_list(backup_dictionary, new_fitnesses_individuals, new_fitnesses)
    if len(backup_dictionary) > len_backup_initial:
        save = Thread(target=save_dictionary_data_compress, args=(working_dictionary, f"{cwd_path}/backup_dict.gzip"))
        print("Opened Thread to save backup dictionary")
        save.start()
        save.join()
        print(f"Dictionary saved as backup_dict.gzip")
    else:
        print("No new fitnesses to save")

    for individual in initial_population:
        fitness = get_fitness(working_dictionary, individual)
        total_fitnesses.append((fitness,))  # fitness is stored as a tuple
                                            # for DEAP eaSimple requirements

    return total_fitnesses
