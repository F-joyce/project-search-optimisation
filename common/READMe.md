# dict_utils module

#### from_csv_db_to_dict()
input : csv with specific format 
output : dictionary with tuples of 450 items as keys and the fitness result as value

Method to extract the database as used in Vladimir implementation of the Genal algorithm and convert it in dictionary

#### check_corruption()
input : dictionary object, a minimum fitness threshold, a maximum fitness threshold
output : tuple : if corrupt-> (True, list of corrupted values), if not corrupt (False, None)
In some runs a bug introduced skewed fitness value in some dictionaries. The main dictionaries are now already clean.
However if necessary this function quickly check if all values in the dictionary are within the range selected.
It is automatically called when running the dictionary compression script.

#### save_dictionary_data() {Better method available -> save_dictionary_data_compress}
input : dictionary, string of filename to write
output : writes a pickle of the dictionary on disk

Saves a dictionary as a pickle with the filename specified, non compressed version.

#### save_dictionary_data_compress()
input : dictionary, string of filename to write
output : writes a pickle of the dictionary on disk

Saves a dictionary as a pickle with the filename specified, compressed with 
gzip format, the pickle written takes up to 40 times less space.

#### load_dictionary_data()
input : filename
output : dictionary object

Loads a pickled uncompressed dictionary to the program. .pickle dictionaries
are loaded with this method

#### load_dictionary_compressed()
input : filename
output : dictionary object

Loads a pickled compressed dictionary to the program. .gzip dictionaries are
loaded with this method

#### add_to_dictionary()
inputs : dictionary, 1 dimension array representing individual configuration,
 fitness value calculated to add to individual configuration output : boolean,
True if the key/value were added, False if the configuration was already present

Add a configuration/fitness to the dictionary, return False if the configuration 
was present already

#### add_to_dictionary_from_list()
inputs : dictionary, list of 1 dimension arrays representing individual 
configurations, list of fitness values calculated to add to individual 
configurations, arrays and corresponding fitness should be stored at the same 
index in the lists
output : a dictionary were all key/value couples in the list are added 
(excluding those already present in the dictionary)

Add a list of configuration/fitness to the dictionary, it won't warn if not 
all fitness were added, however the module using this method is written so 
that it will only use this method with configurations that are not already 
in the dictionary

#### get_fitness()
inputs : dictionary, array or tuple representing the individual configuration
outputs : fitness value of the configuration or False if the key was not found 
in the dictionary

Get the fitness for specified key

#### consistency_check_type()
input : dictionary
output : prints results on terminal

Check if the dictionary keys are all of float types, if not it will convert the keys to 
use floats instead of integers, and if not already present will add them to the dictionary,
then will clean the key integeres entries

#### dict_merger()
input : list of dictionaries, path-filename to output, expected key length (defaults to 450)
output : save a compressed dictionary pickle in gzip with the path/filename provided

this function merges a list of dictionaries into one and save a gzipped pickle
with the path-filename provided

#### dict_merger_files()
input : list of path-filenames of dictionaries, path-filename to output, expected key length (defaults to 450)
output : pass the dictionaries loaded from files to the dict_merger()

Loads dictionaries from disk to pass to dict_merger()

# dict_compressor module
Description: will compress a pickled dictionary to the gzip format reducing 
space usage up to 40 times, checks for corruption calling check_corruption()




