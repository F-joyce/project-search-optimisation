# Description of Project
---
You are in the root folder of the "Barriers Search Optimisation Project".
---
The Project implements different search optimisation techniques:
- Genetic Algorithm (GA) using DEAP python library
- Compositional Pattern Producing Network (CPPN) using NEAT python library
---
The Problems for which solution were found were two:
- find configurations for simulated anti-sismic barriers (BARRIERS)
- find configuration of plates to reduce velocity of bullet impact (PLATES)
TODO:**correct description or extend it**
---
The GA was implemented to work with both BARRIERS and PLATES.

The CPPNs was implemented to only work with BARRIERS.
---
Project Structure:
The common folder stores modules which are shared by all implementations.
Most modules deal with dictionaries, the data structure selected to store
and check configurations.

The subfolders in common are the common files needed by GA or CPPN no matter
what is the variation, this allows to makes changes in one place, while 
having only the script to be modified to make experiments in the "namefolder"
TODO: **decide on a intuitive structure for the project and add description**




















The Project has a partial implementation of RBFOpt this is a:
> RBFOpt is a Python library for black-box optimization 
>(also known as derivative-free optimization).
The partial implementation fails when using more than a small number of
maximum calls of the original function as it needs two different pieces:
1 - Ipoptpy
2 - Bonim solver
The author was unable to install these on the Windows machine used for 
the research. 