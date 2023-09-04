import sys

from common import TESTING

if TESTING:
    print("Initialising plates package, adding plates path ...")
    common_plates_folder = '/Users/fede/Desktop/project-search-optimisation/common/plates'
    sys.path.insert(0, common_plates_folder)
    print("Initialising common package, adding common path ...")
    common_folder = '/Users/fede/Desktop/project-search-optimisation/common'
    sys.path.insert(0, common_folder)

    print("Initialising testing dictionaries")
    plates_dict = {}
    backup_dict = {}
    evaluated = []
else:
    print("Initialising plates package, adding plates path ...")
    common_plates_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/plates'
    sys.path.insert(0, common_plates_folder)
    print("Initialising common package, adding common path ...")
    common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
    sys.path.insert(0, common_folder)
    from dict_utils import load_dictionary_compressed
    print("Loading dictionaries from file")
    plates_dict = load_dictionary_compressed(f"{common_plates_folder}/plates_main_dict.gzip")
    backup_dict = {}
    evaluated = []