import sys

from common import TESTING

if TESTING:
    print("Initialising cppn package, adding cppn path ...")
    common_cppn_folder = '/Users/fede/Desktop/project-search-optimisation/cppn'
    sys.path.insert(0, common_cppn_folder)
    print("Initialising common package, adding common path ...")
else:
    print("Initialising cppn package, adding cppn path ...")
    common_cppn_folder = 'C:/Users/Administrator/Desktop/project-search-optimisation/cppn'
    sys.path.insert(0, common_cppn_folder)