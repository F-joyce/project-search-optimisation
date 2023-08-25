import os
import subprocess
import time

from numpy import savetxt
from utils import reshape_plates_arrays_pop

####################
name_process = 'solve_bullet.py'
name_result_file = 'velocity.txt'
name_conf_file = 'init_state.txt'
HEIGHT_OF_PLATE = 10
WIDTH_OF_PLATE = 50
common_plates_folder = "C:/Users/Administrator/Desktop/project-search-optimisation/common/plates"
####################

def evaluate_pop_fitness(pop):
    pop=reshape_plates_arrays_pop(pop, HEIGHT_OF_PLATE, WIDTH_OF_PLATE)
    iteration = 0
    working_dir_path = os.getcwd()
    fitness = []  
    processes_started = []
    command = "python"
    script_to_run = f"{common_plates_folder}/{name_process}"

      
    for plate_config in pop:
        os.chdir(f"{working_dir_path}/file_{iteration}")
        savetxt('init_state.txt', plate_config, fmt='%.0f')
        processes_started.append(
            subprocess.Popen([command,script_to_run,str(iteration)]))
        iteration += 1  # updates the counter

    iteration = 0  # reset the counter to iterate through all the folders

    for plate_config in pop:
        start_time = time.time()
        minutes = 0
        print(f'Waiting for simulation to output result in file_{iteration}')  
        while not os.path.exists(
                    f"{working_dir_path}/file_{iteration}/{name_result_file}"):
            if time.time()-start_time > 60:
                start_time = time.time()
                minutes += 1
                print(f'Waiting for simulator to output result in file_'
                      f'{iteration} since {minutes} minute(s)')
        
        added = False
        while not added:
            with open(f"{working_dir_path}/file_{iteration}/{name_result_file}"
                      ,'r') as file_:
                try:
                    line = file_.readline().strip()
                    if line != '':
                        fitness_value = ((-1)*float(line)) #unused bias removed
                        processes_started[iteration].kill()
                    fitness.append(fitness_value)
                    print("Appended fitness value for file_%d" %iteration)
                    added = True
                except ValueError:
                    file_.close()

            time.sleep(0.001)
        os.remove(f"{working_dir_path}/file_{iteration}/{name_result_file}")
        os.remove(f"{working_dir_path}/file_{iteration}/{name_conf_file}")
        iteration += 1
    os.chdir(working_dir_path)
    return fitness