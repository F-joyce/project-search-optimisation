import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

import subprocess
import sys
import time
from numpy import savetxt
from threading import Thread

from dict_utils import (save_dictionary_data_compress, 
                        load_dictionary_compressed, 
                        get_fitness, add_to_dictionary_from_list)

cwd_path = os.getcwd()
stored_dict_name = 'storage_dictionary.gzip'
name_process = 'supernova.py'
name_result_file = 'min.txt'
name_conf_file = 'data.csv'



def evaluate_pop_fitness(pop):
    iteration = 0
    working_dir_path = os.getcwd()
    fitness = []
    for configuration in pop:
        print(iteration)
        os.chdir(f"{working_dir_path}/{iteration}")
        savetxt('data.csv', configuration, delimiter=',')
        # shell=True will open processes in the background 
        process = subprocess.Popen([sys.executable, name_process], 
                                   shell=True)
        iteration += 1
    
    iteration = 0

    for configuration in pop:
        start_time = time.time()
        minutes = 0
        print(f'Waiting for simulator to output result in folder {iteration}')
        while not os.path.exists(
                        f'{working_dir_path}/{iteration}/{name_result_file}'):
            if time.time()-start_time > 60:
                start_time = time.time()
                minutes += 1
                print(f'Waiting for simulator to output result in folder'
                      f'{iteration} since {minutes} minute(s)')
        
        added = False
        while not added:
            with open(f'{working_dir_path}/{iteration}/{name_result_file}',
                                                             'r') as file:
                try:
                    fitness_value = float(file.readline().rstrip())
                    fitness.append(fitness_value)
                    print(f'Appended fitness value for folder {iteration}')
                    added = True
                except ValueError:
                    file.close()

            time.sleep(0.001)  # probably to avoid issues ?
        os.remove(f'{working_dir_path}/{iteration}/{name_result_file}')
        os.remove(f'{working_dir_path}/{iteration}/{name_conf_file}') 
        iteration += 1
    os.chdir(working_dir_path)
    return fitness


def batch_fitness_simulation(population, max_batch):
    initial_dictionary = load_dictionary_compressed(f"{cwd_path}/{stored_dict_name}")
    working_dictionary = initial_dictionary.copy()
    initial_population = population.copy()
    total_fitnesses = []
    to_batch_up = []
    for individual in population:
        if get_fitness(initial_dictionary, individual) == False:
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

    working_dictionary = add_to_dictionary_from_list(working_dictionary, to_batch_up, new_fitnesses)
    if len(working_dictionary) > len(initial_dictionary):
        save = Thread(target=save_dictionary_data_compress, args=(working_dictionary, f"{cwd_path}/{stored_dict_name}"))
        print("Opened Thread to save dictionary")
        save.start()
        save.join()
        print(f"Dictionary saved as {stored_dict_name}")
    else:
        print("No new fitnesses to save")

    for individual in initial_population:
        fitness = get_fitness(initial_dictionary, individual)
        total_fitnesses.append((fitness,))  # fitness is stored as a tuple
                                            # for DEAP eaSimple requirements

    return total_fitnesses
