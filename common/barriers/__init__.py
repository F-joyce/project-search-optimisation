from dict_utils import load_dictionary_compressed
import sys

print("Initialising plates package, adding plates path ...")
common_barrier_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/barriers'
sys.path.insert(0, common_barrier_folder)

print("Loading dictionaries from file")
barrier_dict = load_dictionary_compressed(f"{common_barrier_folder}/barriers_main_dict.gzip")
backup_dict = {}