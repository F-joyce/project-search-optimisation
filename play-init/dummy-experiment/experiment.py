import sys, os
common_folder = "/Users/fede/Desktop/project-search-optimisation/play-init/root/common"
sys.path.insert(0, common_folder)

from pack1.module1 import call_manipulate_data

call_manipulate_data()

from pack1 import data_to_manipulate, backup

print(data_to_manipulate)
print(backup)

