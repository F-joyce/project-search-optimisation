import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

from dict_utils import (load_dictionary_compressed,
                        dict_merger)

def dict_merger_files(list_dict_files, filename_to_save, expected_key_length=450):
    dictionaries = []
    for dict_file in list_dict_files:
        to_add = load_dictionary_compressed(list_dict_files)
        dictionaries.append(to_add)
    dict_merger(dictionaries, filename_to_save, expected_key_length)