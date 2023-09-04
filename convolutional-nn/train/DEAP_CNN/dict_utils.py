import pandas as pd
import numpy as np
import pickle

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

def save_dictionary_data(dictionary, name_dict="initial_dictionary.pickle"):
    with open(name_dict, 'wb') as file:
        pickle.dump(dictionary, file)
    return True

def load_dictionary_data(name_dict="initial_dictionary.pickle"):
    with open(name_dict, "rb") as file:
        dictionary = pickle.load(file)
    return dictionary

def add_to_dictionary(dictionary, array, fitness):
    tuple_to_add = tuple(array)
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
    array = np.asfarray(array)
    if type(array) != tuple:
        key = tuple(array)
    else:
        key = array
    if key in dictionary.keys():
        fitness = dictionary[key]
        return fitness
    else:
        return False
    
    


