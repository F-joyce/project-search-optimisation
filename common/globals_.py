from dict_utils import load_dictionary_compressed

common_barrier_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/barriers'
common_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common'
common_plates_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/common/plates'

plates_dict = load_dictionary_compressed(f"{common_plates_folder}/plates_main_dict.gzip")
barrier_dict = load_dictionary_compressed(f"{common_barrier_folder}/barriers_main_dict.gzip")
backup_dict = {}