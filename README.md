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

### Barriers and Plates packages
The packages are organised in a very similar way, the common features will be described here. Then the modules which are specific to the packages in the next section.
#### __init__
Initialise the paths to a path or another depending if TESTING is on or off. TESTING should be changed manually directly in the templates (e.g. GA_barriers_template, and not in the __init__ files. However the paths are hard coded in the init files, they point to the specific remote machine used to make experiements, and to the local machine used to develop the modules. These should be changed to when a new machine is used. When TESTING is set to True, the search will happen but no simulation will start, instead a dummy fitness function is used for quick result. This is useful when checking the script are working as expected, for example when introducing some change in the common modules.
#### barriers/plates_evaluate

####
####
####
####

### Plates package
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
















The Project has a partial implementation of RBFOpt this is a:
> RBFOpt is a Python library for black-box optimization 
>(also known as derivative-free optimization).
The partial implementation fails when using more than a small number of
maximum calls of the original function as it needs two different pieces:
1 - Ipoptpy
2 - Bonim solver
The author was unable to install these on the Windows machine used for 
the research. 