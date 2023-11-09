import pandas as pd
import numpy as np
import pickle
import gzip

def from_csv_db_to_dict(name_db = "./dataframes/database.csv"):
    db = pd.read_csv(name_db)
    db.drop(columns=db.columns[0], axis=1, inplace=True)
    list_full = []
    list_uniques_full = []
    for index, row in db.iterrows():
        list_full.append(row.values)
    for row_full in list_full:
        for item in list_uniques_full:
            if np.array_equal(row_full, item):
                break
        else:
            list_uniques_full.append(row_full)
    barriers_dictionary = {}
    for arrays in list_uniques_full:
        tuple_key = (tuple(arrays[:450]))
        fitness_value = arrays[450].item()
        #assert type(tuple_key)== tuple, "The key is not a tuple"
        #assert type(fitness_value) == float, "Not a float"
        barriers_dictionary[tuple_key] = fitness_value
    return barriers_dictionary


def check_corruption(dictionary, min_realistic_value, max_realistic_value):
    corrupted = False
    corrupt_values = []
    for value in dictionary.values():
        if value > min_realistic_value or value < max_realistic_value:
            corrupted = True
            corrupt_values.append(value)
    if corrupted:
        return corrupted, corrupt_values
    else:
        return corrupted, None
    

def save_dictionary_data(dictionary, name_dict="initial_dictionary.pickle"):
    with open(name_dict, 'wb') as file:
        pickle.dump(dictionary, file)
    return True

def save_dictionary_data_compress(dictionary, name_dict="initial_dictionary.pickle"):
    with gzip.open(name_dict, 'w', compresslevel=1) as file:
        pickle.dump(dictionary, file, protocol=pickle.HIGHEST_PROTOCOL)
    return True


def load_dictionary_data(name_dict="initial_dictionary.pickle"):
    with open(name_dict, "rb") as file:
        dictionary = pickle.load(file)
    return dictionary


def load_dictionary_compressed(filename):
        """Resumes the simulation from a previous saved point."""
        with gzip.open(filename) as file:
            data = pickle.load(file)
            return data


def add_to_dictionary(dictionary, array, fitness):
    farray = np.asfarray(array)
    flattened_farray = farray.flatten()
    tuple_to_add = tuple(flattened_farray)
    if tuple_to_add in dictionary.keys():
        return False
    else:
        dictionary[tuple_to_add] = fitness
        return True
    
def add_to_dictionary_from_list(dictionary, list_arrays, list_fitnesses):
    for array,fitness in zip(list_arrays, list_fitnesses):
        add_to_dictionary(dictionary, array, fitness)
    return dictionary

def get_fitness(dictionary, array):
    farray = numpy.asfarray(array)
    flattened_farray = farray.flatten()
    key = tuple(flattened_farray)
    #print("Key is")
    #print(key)
    if key in dictionary.keys():
        fitness = dictionary[key]
        return fitness
    else:
        return False

import numpy

def consistency_check_type(data):
    num_initial = len(data)
    list_keys_inconsistent = []
    for each_key in data.keys():
        try:
            assert isinstance(each_key[0], (numpy.floating,float)), f"The key was of type {type(each_key[0])}"
        except AssertionError:
            list_keys_inconsistent.append(each_key)
    num_in = len(list_keys_inconsistent)

    print("In the initial dictionary are stored %s items, the number of \
non_float entries found is %s" % (num_initial, num_in))

    if num_in > 0:
        for each_integer_key in list_keys_inconsistent:
            as_farray = numpy.asfarray(each_integer_key)
            as_flattened_farray = as_farray.flatten()
            as_tuple = tuple(as_flattened_farray)
            fitness = get_fitness(data, each_integer_key)
            del data[each_integer_key]
            add_to_dictionary(data, as_tuple, fitness)
        num_final_data = len(data)
        diff = num_initial-num_final_data
        message = (f'The dictionary has now consistent keys of one type of float. '
                f'It stores {num_final_data} items. {diff} doubles were found')
        print(message)

    print("Dictionary consistency check completed")


def dict_merger(list_dicts:list, filename:str, expected_key_length = 450):
    tot_len = 0
    for dict_ in list_dicts:
        assert len(next(iter(dict_))) == expected_key_length, "The key is not" \
                                                                "of the expected length"
        tot_len+=len(dict_)
    cumulative_dictionary = {k: v for d in list_dicts for k, v in d.items()}
    consistency_check_type(cumulative_dictionary)
    cum_len = len(cumulative_dictionary)
    save_dictionary_data_compress(cumulative_dictionary, filename)
    print("The sum of length of dictionaries was %s, the len of the cumulative dictionary is %s" % (tot_len, cum_len))


def dict_merger_files(list_dict_filenames, filename_to_save, expected_key_length=450):
    dictionaries = []
    for dict_file in list_dict_filenames:
        to_add = load_dictionary_compressed(dict_file)
        dictionaries.append(to_add)
    dict_merger(dictionaries, filename_to_save, expected_key_length)