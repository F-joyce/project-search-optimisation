import sys, os
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
sys.path.insert(0, common_folder)

import pandas as pd
import numpy as np
import pickle
import gzip
import re
from dict_utils import (load_dictionary_compressed, load_dictionary_data,
                        save_dictionary_data_compress, check_corruption)

#################### TO BE ADJUSTED BY TASK
MAX_VALUE = 130
MIN_VALUE = 20
name_dictionary = 'bullets_dictionary.pickle'
new_name_dictionary = re.sub('pickle', 'gzip', name_dictionary)
####################

dict_data = load_dictionary_data(name_dictionary)  
corrupted, list_corrupt = check_corruption(dict_data, MAX_VALUE, MIN_VALUE) 
if not corrupted:
    save_dictionary_data_compress(dict_data, new_name_dictionary)
    data_loaded = load_dictionary_compressed(new_name_dictionary)
    assert len(dict_data) == len(data_loaded)
else:
    print("The dictionary has corrupted values", list_corrupt)
