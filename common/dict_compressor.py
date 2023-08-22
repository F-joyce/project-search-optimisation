import pandas as pd
import numpy as np
import pickle
import gzip
import re

def load_dictionary_data(name_dict="initial_dictionary.pickle"):
    with open(name_dict, "rb") as file:
        dictionary = pickle.load(file)
    return dictionary

def save_dictionary_data_compress(dictionary, name_dict="initial_dictionary.pickle"):
    with gzip.open(name_dict, 'w', compresslevel=5) as file:
        pickle.dump(dictionary, file, protocol=pickle.HIGHEST_PROTOCOL)
    return True

def load_dictionary_compressed(filename):
        """Resumes the simulation from a previous saved point."""
        with gzip.open(filename) as file:
            data = pickle.load(file)
            return data
        

name_dictionary = 'dictionary.pickle'
new_name_dictionary = re.sub('pickle', 'gzip', name_dictionary)

dict_data = load_dictionary_data(name_dictionary)

def check_corruption(diction, thresholds_array):
    corrupted = False
    corrupt_values = []
    for value in diction.values():
        if value > thresholds_array[0] or value < thresholds_array[1]:
            corrupted = True
            corrupt_values.append(value)
    if corrupted:
        return corrupted, corrupt_values
    else:
        return corrupted, None
    
corrupted, list_corrupt = check_corruption(dict_data, [-0.1e-08, -4.9e-08])

if not corrupted:
    save_dictionary_data_compress(dict_data, new_name_dictionary)

    data_loaded = load_dictionary_compressed(new_name_dictionary)

    assert len(dict_data) == len(data_loaded)
else:
    print("The dictionary has corrupted values", list_corrupt)
