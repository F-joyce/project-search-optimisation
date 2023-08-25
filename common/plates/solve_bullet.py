import math
import os
import sys

config_num=int(sys.argv[1])
location = os.path.dirname(os.getcwd())
os.chdir(location + "/file_" + str(config_num))

os.system("C:/Users/Administrator/Desktop/1_1mat_opt_princ/lsdyna.exe I="+location+"/lsd1.k ncpu=1 memory=256M")

# reading results from a special file and retrieving velocity from kinetic energy
if os.path.isfile("matsum") and os.stat('matsum').st_size > 20000:
    f = open('matsum', 'r')
    time_counter = 0
    while 1:
        line = f.readline().strip()
        vals = line.split(' ')
        if vals[0] == 'time':
            time_counter += 1
            if float(vals[4]) >= 1.44E-4:
                line = f.readline().strip()
                vals = line.split(' ')
                E = float(vals[28])
                velocity = math.sqrt(E/0.1515)
                f.close()
                break
else:
    print("Encountered an issue running Lsdyna.")
    velocity = 1000

print(velocity)
f = open("velocity.txt", "w")
f.write(str(velocity))
f.close()


