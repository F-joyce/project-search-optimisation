from dict_utils import load_dictionary_compressed
import os

POPULATION = 200
MAX_BATCH = 200
GENERATIONS = 5
CX_PROBABILITY = 0.7
MUT_PROBABILITY = 0.15
BIT_MUT_PROBABILITY = 0.1
TOURN_SIZE = 3
CX_TYPE = "cxTwoPoint"

parameters = 500
nmaterials = 2
shape = (25,20) # vertical,horizontal
percentages_ranges = [(80,90),(0,10)]#,(0,10),(0,10),(0,10),(0,10)]

name_conf_file = "data.txt"
name_result_file = "min.txt"
name_process = "supernova_dry.py"
experiment_path = os.getcwd()
dummy_dict_path = f"{experiment_path}/barriers_dummy_dict.gzip"

seeded = False

try:
    barriers_dict = load_dictionary_compressed(f"{experiment_path}/barriers_dummy_dict.gzip")
except:
    barriers_dict = {}
backup_dict = {}
evaluated = []
