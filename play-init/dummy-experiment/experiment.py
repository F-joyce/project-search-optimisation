import sys
common_folder = "/Users/fede/Desktop/project-search-optimisation/play-init/root"
sys.path.insert(0, common_folder)

print(sys.path)

import common
from common.pack1.module1 import call_manipulate_data

print(sys.path)

call_manipulate_data()


from common.pack1 import data_to_manipulate, backup

print(data_to_manipulate)
print(backup)

