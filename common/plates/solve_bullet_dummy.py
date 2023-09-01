import math
import os
import sys
import random

config_num=int(sys.argv[1])
#from plates import common_plates_dir
location = os.path.dirname(os.getcwd())
os.chdir(location + "/file_" + str(config_num))

#os.system("C:/Users/Administrator/Desktop/1_1mat_opt_princ/lsdyna.exe I="+common_plates_dir+"/lsd1.k ncpu=1 memory=256M")

# reading results from a special file and retrieving velocity from kinetic energy
velocity = random.choice(range(100))

print(velocity)
f = open("velocity.txt", "w")
f.write(str(velocity))
f.close()


