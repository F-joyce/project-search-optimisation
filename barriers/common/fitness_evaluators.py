import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

import os
import subprocess
import sys
import time
import numpy as np

from numpy import savetxt
from threading import Thread

from dict_utils import (save_dictionary_data_compress, load_dictionary_compressed, 
                        get_fitness, add_to_dictionary_from_list)

dictionary = load_dictionary_compressed('updated_dictionary.pickle')

def cal_pop_fitness(pop):

    path = os.getcwd()

    fitness = []
    loopar = 0
    for Bshape in pop:
        print(loopar)
        os.chdir(path+'/'+str(loopar))
        savetxt('data.csv', Bshape, delimiter=',')
        pid = subprocess.Popen([sys.executable, "supernova.py"])
        print("After subprocess.Popen for loop number %d" %loopar)
        loopar += 1  # updates the counter

    loopar = 0  # reset the counter to iterate through all the folders

    for Bshape in pop:  
        while not os.path.exists(path+'/'+str(loopar)+'/min.txt'):
            print(path+'/'+str(loopar)+'/min.txt')
            time.sleep(5)
        
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