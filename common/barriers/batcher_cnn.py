import os
import numpy as np  
from threading import Thread
from dict_utils import (save_dictionary_data_compress, 
                        get_fitness, add_to_dictionary_from_list)

from barriers_evaluate import evaluate_pop_fitness
import barriers
from cnn_evaluate import cal_pop_fitness_CNN

cwd_path = os.getcwd()

def batch_fitness_simulation(population, max_batch):
    working_dictionary = barriers.barriers_dict
    backup_dictionary = barriers.backup_dict
    cnn_dict = barriers.cnn_dictionary
    len_backup_initial = len(backup_dictionary)
    evaluated_ind = barriers.evaluated
    initial_population = population.copy()
    total_fitnesses = []
    to_batch_up = []
    for individual in population:
        if get_fitness(working_dictionary, individual) == False:
            to_batch_up.append(individual)
    new_fitnesses = []
    new_fitnesses_individuals = to_batch_up.copy()
    cnn_fitnesses = cal_pop_fitness_CNN(new_fitnesses_individuals)
    cnn_dict = add_to_dictionary_from_list(cnn_dict, new_fitnesses_individuals, cnn_fitnesses)
    to_remove = []
    for i in to_batch_up:
        cnn_fitness = get_fitness(cnn_dict, i)
        if cnn_fitness < -1.45e-08:
            to_remove.append(i)
    for remove in to_remove:
        to_batch_up.remove(remove)
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
        save = Thread(target=save_dictionary_data_compress, args=(backup_dictionary, f"{cwd_path}/backup_dict.gzip"))
        print("Opened Thread to save backup dictionary")
        save.start()
        save.join()
        print(f"Dictionary saved as backup_dict.gzip with {len(backup_dictionary)} configurations")
    else:
        print("No new fitnesses to save")

    for individual in initial_population:
        if individual in evaluated_ind:
            pass
        else:
            evaluated_ind.append(individual)

        fitness = get_fitness(working_dictionary, individual)
        if not fitness:
            fitness = get_fitness(cnn_dict, individual)
        total_fitnesses.append((fitness,))  # fitness is stored as a tuple
                                            # for DEAP eaSimple requirements

    return total_fitnesses