import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

import subprocess
import sys
import time
from numpy import savetxt

name_process = 'supernova.py'
name_result_file = 'min.txt'
name_conf_file = 'data.csv'

def evaluate_pop_fitness(pop):
    iteration = 0
    working_dir_path = os.getcwd()
    fitness = []
    for configuration in pop:
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
                print(f'Waiting for simulator to output result in folder '
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