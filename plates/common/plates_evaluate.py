import os
import subprocess
import time
import numpy as np

from numpy import savetxt
from specific.utils import reshape_plates_arrays_pop

####################
name_process = 'solve_bullet.py'
name_result_file = 'velocity.txt'
name_conf_file = 'init_state.txt'
HEIGHT_OF_PLATE = 10
WIDTH_OF_PLATE = 50
####################

def evaluate_pop_fitness(pop):
    pop=reshape_plates_arrays_pop(pop, HEIGHT_OF_PLATE, WIDTH_OF_PLATE)
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