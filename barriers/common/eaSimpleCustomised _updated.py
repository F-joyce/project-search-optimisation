import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

import subprocess
import sys
import time
from numpy import savetxt
from threading import Thread

from dict_utils import (save_dictionary_data_compress, load_dictionary_compressed, 
                        get_fitness, add_to_dictionary_from_list)


def cal_pop_fitness(pop):
    loopar = 0
    path = os.getcwd()  # works where the script is run from
    fitness = []  # empty list for fitnesses
    for Bshape in pop:
        print(loopar)
        os.chdir(path+'/'+str(loopar))
        savetxt('data.csv', Bshape, delimiter=',')
        pid = subprocess.Popen([sys.executable, "supernova.py"], shell=True)
        loopar += 1  # updates the counter

    loopar = 0  # reset the counter to iterate through all the folders

    for Bshape in pop:  # iterate through all the folders just created to save the fitness found in the min.txt files in the list fitness
        # check the file exist, waits until it does, this file is most likely an output of the supernova2M.py script
        start_time = time.time()
        minutes_counter = 0
        print(f'Waiting for simulator to output result in folder {loopar}')
        while not os.path.exists(path+'/'+str(loopar)+'/min.txt'):
            if time.time()-start_time > 60:
                start_time = time.time()
                minutes_counter += 1
                print(f'Waiting for simulator to output result in folder {loopar} since {minutes_counter} minute(s)')
        
        added = False
        while not added:
            with open(path+'/'+str(loopar)+'/min.txt', 'r') as f:
                try:
                    fitness_value = float(f.readline().rstrip())
                    fitness.append(fitness_value)
                    print("Appended fitness value for folder %d" %loopar)
                    added = True
                except ValueError:
                    f.close()

            time.sleep(0.001)  # probably to avoid issues ?
        os.remove(path+'/'+str(loopar)+'/min.txt')  # delete the min.txt file
        os.remove(path+'/'+str(loopar)+'/data.csv')  # delete the data.csv file
        loopar += 1
    os.chdir(path)
    return fitness

def batch_fitness_simulation(population, max_batch):
    dictionary = load_dictionary_compressed('storage_dictionary.gzip')
    working_dictionary = dictionary.copy()
    initial_population = population.copy()
    total_fitnesses = []
    to_batch_up = []
    for individual in population:
        if get_fitness(dictionary, individual) == False:
            to_batch_up.append(individual)
    new_fitnesses = []
    new_fitnesses_individuals = to_batch_up.copy()
    loopar = 0
    while len(to_batch_up) > 0:
        print("There are %d unseen configuration to simulate" % len(to_batch_up))
        temp_list = []
        while (len(temp_list) < max_batch) and (len(to_batch_up) > 0):
            temp_list.append(to_batch_up.pop(0))
        fitnesses_to_append = cal_pop_fitness(temp_list)
        for fitness_value in fitnesses_to_append:
            new_fitnesses.append(fitness_value)

    print("The new fitnesses put in a list are: ", len(new_fitnesses))
    print("The individual to be calculated were: ", len(new_fitnesses_individuals))

    working_dictionary = add_to_dictionary_from_list(dictionary, to_batch_up, new_fitnesses)
    if len(working_dictionary) == 0:
        working_dictionary = add_to_dictionary_from_list(dictionary, new_fitnesses_individuals, new_fitnesses)
    else:
        working_dictionary = add_to_dictionary_from_list(working_dictionary, new_fitnesses_individuals, new_fitnesses)
    
    save = Thread(target=save_dictionary_data, args=(working_dictionary, "dictionary.pickle"))
    print("SAVING DICTIONARY")
    save.start()
    save.join()
    print("SAVING COMPLETED")

    for individual in initial_population:
        fitness = get_fitness(dictionary, individual)
        total_fitnesses.append((fitness,))

    return total_fitnesses