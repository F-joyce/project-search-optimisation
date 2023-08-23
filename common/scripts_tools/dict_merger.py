import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

import random
import numpy
from dict_utils import (load_dictionary_data, load_dictionary_compressed, get_fitness,
                         add_to_dictionary, save_dictionary_data_compress)

dicts_names = []
dicts = []
tot_len = 0

expected_key_length = 450

for filename in dicts_names:
    to_add = load_dictionary_compressed(filename)
    assert len(next(iter(to_add))) == expected_key_length, "The key is not" \
                                                            "of the expected length"
    tot_len+=len(to_add)
    dicts.append(to_add)

cumulative_dictionary = {k: v for d in dicts for k, v in d.items()}
cum_len = len(cumulative_dictionary)
save_dictionary_data_compress(cumulative_dictionary, "cumulative_dict")
print("The sum of length of dictionaries was %s, the len of the cumulative dictionary is %s" % (tot_len, cum_len))