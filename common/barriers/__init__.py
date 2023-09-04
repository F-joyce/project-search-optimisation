import sys

from common import TESTING

if TESTING:
    print("Initialising barriers package, adding barriers path ...")
    common_barriers_folder = '/Users/fede/Desktop/project-search-optimisation/common/barriers'
    sys.path.insert(0, common_barriers_folder)
    print("Initialising common package, adding common path ...")
    common_folder = '/Users/fede/Desktop/project-search-optimisation/common'
    sys.path.insert(0, common_folder)

    print("Initialising testing dictionaries")
    barriers_dict = {}
    backup_dict = {}
    cnn_dictionary = {}
    evaluated = []
else:
    print("Initialising barriers package, adding barriers path ...")
    common_barriers_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/barriers'
    sys.path.insert(0, common_barriers_folder)
    print("Initialising common package, adding common path ...")
    common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
    sys.path.insert(0, common_folder)
    from dict_utils import load_dictionary_compressed
    print("Loading dictionaries from file")
    barriers_dict = load_dictionary_compressed(f"{common_barriers_folder}/barriers_main_dict.gzip")
    backup_dict = {}
    evaluated = []