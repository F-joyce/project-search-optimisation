# Description of Project
---
You are in the root folder of the "Barriers Search Optimisation Project".
---
The Project implements two different search optimisation techniques:
- Genetic Algorithm (GA) using DEAP python library
- Compositional Pattern Producing Network (CPPN) using NEAT python library
---
The Problems for which solution were found are two:
- find configurations for simulated anti-sismic barriers (BARRIERS)
- find configuration of plates to reduce velocity in simulated bullet impact (PLATES)
TODO:**correct description or extend it**
---
The GA was implemented to work with both BARRIERS and PLATES.

The CPPNs was implemented to only work with BARRIERS.
---

# Quick start usage
Barriers problem solved with a genetic algorithm will be used as an example, this is an actual run and not a ""dry-run". 
1. Go to the genetic-algorithm folder, copy GA_barries_template or GA_barriers_experiment_templates for multiple run. 
2. Paste it in any folder in the system. 
3. If the machine used for experiments is not the original Windows machine. Change the paths in the common/barriers/__init__.py
4. If on Windows, click on the path section and write cmd, press Return/Enter
5. At the command prompt (it should have appeared) write <code>python Ga_barriers_template.py</code>
6. The script will start. After path initialisation the ga will open a bunch of script running the simulation. In the command prompt at some point will appear <code>Waiting for simulation to output results since X minutes</code>. If X is larger than 7 minutes, probably one of the scripts got stuck, this can usually be pushed forward by finding a stuck script and pressing Return ***TODO*** add screenshot of what this will look like.

# Project Structure:
## The common package stores modules which are used by the implementations. 

### Barriers and Plates similar modules

The packages are organised in a very similar way, the common features will be described here. What changes is from where some methods are imported, for example the evaluate_pop_fitness will be imported from the barrier package for barriers and from plates package for plates and so on. Modules with different structure for different packages are explained in next sections.

#### __init__

Initialise the paths to a path or another depending if TESTING is on or off. TESTING should be changed manually directly in the templates (e.g. GA_barriers_template, and not in the __init__ files. However the paths are hard coded in the init files, they point to the specific remote machine used to make experiements, and to the local machine used to develop the modules. These should be changed to when a new machine is used. When TESTING is set to True, the search will happen but no simulation will start, instead a dummy fitness function is used for quick result. This is useful when checking the script are working as expected, for example when introducing some change in the common modules.

The init also load the main dictionaries from file or initialised an empty one when testing.
Also initialised a backup_dictionary and an evaluated list, more on this on the batcher description.

#### batcher

Batcher method <code>batch_fitness_simulation()</code> in brief return the fitnesses of a population of individuals to the eaSimple algorithm.
1. It checks if the individuals are stored with a fitness in the dictionary (previously simulated)
2. Add individuals still to be simulated in a list
3. Chop up this list depending on the variable MAX_BATCH
4. Send the smaller list to be evaluated by the evaluate function
5. At the end of all the batches, updates the dictionaries and return the fitnesses for the individuals

The main dictionaries(working_dictionaries) are retrieved from the packages (init files) to be updated and shared between modules.
These are not saved until the end of the main script as loading and saving can be time consuming.
The backup dictionary holds the individuals simulated in the run, this gets saved at each generation (batcher cycle) in the experiment folder, to avoid loss of fitnesses in case the main script get stuck or blocked for any reason. The script merge_dictionaries can be used to merge a stored dictionary and a backup one if something goes wrong.
Evaluated is use to manually count how many samples the whole script simulates. This is useful with the cppn, as it does not store the evaluation numbers automatically.

#### eaSimpleCustomised

This should not be touched directly, it allow the DEAP library work with ANSYS. The fitness function is inserted manually here the batch_fitness_simulation. In this way it's possible to have manual control on how many processes get started on ANSYS and to retrieve from dictionary when available and all that is done in the batcher module.

#### GA_templates

The main script executed to run the experiments. This is what it does:
1. TESTING set to True or False, run a real simulation or a dry-run(dummy fitness fucntion). This will change paths for dictionaries etc.
2. Set the root folder of the project, this should be changed manually if the main folder is moved.
3. Import the common package (__init__) and set the TESTING constant
4. Import the path from the barrier package
5. Set the parameters for the process (number of parallel simulation) 
6. Set the parameters for the genetic algorithm
7. Set the way individual in the population are initialised
8. Folders are created and files copied as necessary
9. Run the genetic algorithm with DEAP, some parameters can be changed only in this part, knowledge of DEAP library is required
9. Save data and statistics at the end of the run and plot a graph (if not an experiment)

## Barrier specific
#### barriers_evaluate and supernova
These modules work strictly together. 
barriers_evaluate save the individual configuration as a data.csv file in a separate folder. 
The number of folders correspond by the amount of simulation to be run in parallel and depends by the MAX_BATCH variable. 
As each simulation takes up to 100GB of space in the disk, the MAX_BATCH has to be carefully selected (in the template. 
Data.csv file is read by supernova, this is the script that launch the ANSYS simulator and is copied in each folder at the beginning at execution of the main module. It holds the parameters for the simulation to be run. The simulation is launched and supernova extract the resulting fitness from the simulation in a min.txt file that gets picked up by barriers_evaluate and returned to the batcher.

## Plates specific
#### plates_evaluate and solve_bullet
As for barriers_evaluate and supernova.
However some key differences:
- solve_bullet is not copied to the folders
- the configuration is saved as init_state.txt
- the result of the simulation is saved as velocity.txt
- a HEIGHT and WIDTH are necessary to specify the 2 dimesnions of the plates
- the process won't open new windows but will run directly in the command prompt when the template is executed
- the simulation don't take as much space, the limit here is set by CPU number more than storage
#### customMutation
This works as a flipbit mutation except preserving a specific set of bits to 1, this is necessary for the simulation, as represent the point of impact of the bullet.
The subfolders in common are the common files needed by GA or CPPN no matter
what is the variation, this allows to makes changes in one place, while 
having only the script to be modified to make experiments in the "namefolder"
TODO: **decide on a intuitive structure for the project and add description**

### Script tools

# Refactoring ideas
### Switch to JSON
this entails some difficulty as JSON key are string and for current dictionaries
tuples were used. The switch is not straightforward and requires building ad-hoc
testing before trying to implement the change. Possible issues:
- key need to be retrieved in integer and float format, 1,0,1 should be equivalent to 1.,0.,1.
  this is straightforward with tuples, much less with strings as keys
- key need to be stored in a consistent way
Advantages of JSON are mostly of speed in loading and dumping the data.

### Globals __init__.py not working as would be ideal
The packages get loaded twice instead of accessing the variable that is already been initialised.
It's working witht the current implementation but can be imagine to lead to issues along the way.

### Add an integration test
Testing on the complete execution is now manually explored. Would be useful to add some assert statement and checks, printing at the end, to confirm all is running as expected. Test to add:
- the dictionaries has been updated with the exact number of new fitnesses found
- ***TODO*** add more















# Issues with RBFOpt
The Project has a partial implementation of RBFOpt this is a:
> RBFOpt is a Python library for black-box optimization 
>(also known as derivative-free optimization).
The partial implementation fails when using more than a small number of
maximum calls of the original function as it needs two different pieces:
1 - Ipoptpy
2 - Bonim solver
The author was unable to install these on the Windows machine used for 
the research. 