import os
import numpy as np
import subprocess
import sys
import time
from threading import Thread

from dict_utils import get_fitness, add_to_dictionary_from_list

import config

name_conf_file = config.name_conf_file
name_process = config.name_process
name_result_file = config.name_result_file

barriers_dict = config.barriers_dict
backup_dict = config.backup_dict
evaluated = config.evaluated
experiment_path = config.experiment_path
log = config.data_object

def function_that_evaluate_population(pop):
    iteration = 0
    working_dir_path = os.getcwd()
    fitness = []
    for configuration in pop:
        os.chdir(f"{working_dir_path}/processes/{iteration}")
        # np.savetxt(name_conf_file, configuration, delimiter=',')
        np.savetxt(name_conf_file, configuration)
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
    # if len(backup_dictionary) > len_backup_initial:
    #     save = Thread(target=save_dictionary_data_compress, args=(backup_dictionary, f"{experiment_path}/backup_dict.gzip"))
    #     print("Opened Thread to save backup dictionary")
    #     save.start()
    #     save.join()
    #     print(f"Dictionary saved as backup_dict.gzip with {len(backup_dictionary)} configurations")
    # else:
    #     print("No new fitnesses to save")

    initial_eval_value = len(evaluated_ind)

    log.increaseGen()

    for individual in initial_population:
        
        if isinstance(individual, np.ndarray):
            individual = individual.tolist()
        if individual in evaluated:
            pass
        else:
            evaluated_ind.append(individual)
            
        fitness = get_fitness(working_dictionary, individual)
        log.updateHighLow(fitness, tuple(individual))
        total_fitnesses.append((fitness,))  # fitness is stored as a tuple
                                            # for DEAP eaSimple requirements
    
    unique_evaluations = len(evaluated_ind) - initial_eval_value
    log.saveGeneration(unique_evaluations)

    return total_fitnesses