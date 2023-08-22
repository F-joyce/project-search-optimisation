import sys, os
common_folder = ""
sys.path.insert(0, common_folder)

import random
import numpy
from dict_utils import (load_dictionary_compressed, get_fitness,
                         add_to_dictionary, save_dictionary_data_compress)

name_dictionary = 'dictionary.gzip'
path_to_dictionary = os.getcwd()

data = load_dictionary_compressed(f'{path_to_dictionary}/{name_dictionary}')

num_initial = len(data)

list_keys_inconsistent = []

for each_key in data.keys():
    try:
        assert isinstance(each_key[0], (numpy.floating,float)), f"The key was of type {type(each_key[0])}"
    except AssertionError:
        list_keys_inconsistent.append(each_key)

num_in = len(list_keys_inconsistent)

print("In the dictionary are stored %s items, the number of \
inconsistent entries found is %s" % (num_initial, num_in))

if num_in > 0:
    for each_integer_key in list_keys_inconsistent:
        as_farray = numpy.asfarray(each_integer_key)
        as_tuple = tuple(as_farray)
        isin = get_fitness(data, as_tuple)
        if not isin:
            fitness = get_fitness(data, each_integer_key)
            add_to_dictionary(data, as_farray, fitness)
            del data[each_integer_key]
        else:
            del data[each_integer_key]

    num_final_data = len(data)
    diff = num_initial-num_final_data

    name_new_dictionary = f"cleaned_{name_dictionary}"

    save_dictionary_data_compress(data, f'{common_folder}/{name_new_dictionary}')

    message = (f'The dictionary has now consistent keys of numpy.float64 type. '
               f'It stores {num_final_data} items. The number of keyvalue cleaned ' 
               f'is {diff}. The new dictionary was saved with prefix cleaned_')
    print(message)

print("Dictionary consistency check completed")