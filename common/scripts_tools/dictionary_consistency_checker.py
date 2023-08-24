import sys
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

import numpy
from dict_utils import (get_fitness, add_to_dictionary)

def consistency_check(data):
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
        message = (f'The dictionary has now consistent keys of one type of float. '
                f'It stores {num_final_data} items. The number of keyvalue cleaned ' 
                f'is {diff}.')
        print(message)

    print("Dictionary consistency check completed")
