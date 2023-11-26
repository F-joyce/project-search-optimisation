from dict_utils import load_dictionary_compressed
from data_handler import DataRun
import os

#UNIVERSAL PARAMETERS
data_object = DataRun("run_logs")

POPULATION = 80
GENERATIONS = 5
MAX_BATCH = 40
nmaterials = 5
shape = (5,5) # vertical,horizontal
parameters = shape[0]*shape[1]
name_conf_file = "data.txt"
name_result_file = "min.txt"
name_process = "supernova_dry.py"
experiment_path = os.getcwd()
dummy_dict_path = f"{experiment_path}/barriers_dummy_dict.gzip"
backup_dict_path = f"{experiment_path}/backup/last_working_main.gzip"
try:
    barriers_dict = load_dictionary_compressed(f"{experiment_path}/barriers_dummy_dict.gzip")
except:
    barriers_dict = {}

backup_dict = {}
evaluated = []

# GA-only PARAMETERS
CX_PROBABILITY = 0.7
MUT_PROBABILITY = 0.15
BIT_MUT_PROBABILITY = 0.1
TOURN_SIZE = 3
CX_TYPE = "cxTwoPoint"

percentages_ranges = [(80,90),(0,10)]#,(0,10),(0,10),(0,10),(0,10)]

seeded = False

# CPPN-only PARAMETERS
full_scale = 15
nocrossover = False


