from ... import common
from dict_utils import load_dictionary_compressed
import sys

print("Initialising plates package, adding plates path ...")
common_plates_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/plates'
sys.path.insert(0, common_plates_folder)

print("Loading dictionaries from file")
plates_dict = load_dictionary_compressed(f"{common_plates_folder}/plates_main_dict.gzip")
backup_dict = {}