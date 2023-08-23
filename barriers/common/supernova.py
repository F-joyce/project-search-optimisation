import warnings
import os
import datetime
import time
import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from ansys.mapdl import core as pymapdl
    from ansys.mapdl.core import launch_mapdl

    new_path = 'C:/Program Files/ANSYS Inc/v182/ansys/bin/winx64/ansys182.exe'
    pymapdl.change_default_ansys_path(new_path)


def print_time():
	return datetime.datetime.now().strftime("%H:%M:%S")


print(f'Started simulation at {print_time()}')
path = os.getcwd()
num_processor = 2

mapdl = None
while mapdl is None:
	try:
		time.sleep(5)
		print(path)
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			mapdl = launch_mapdl(nproc=num_processor,run_location=path,additional_switches="-p ane3flds",
								 mode='corba',override=True, jobname=f"barrier")
	except Exception as e:
		print(str(e))
		pass

mapdl.run('finish')
mapdl.run('/clear,start')
mapdl.run('/PREP7')
mapdl.run('youngSoil=1.0e10')
mapdl.run('poiss=0.35')
mapdl.run('densSoil=2000.0')
mapdl.run('youngBarr=10.0e10')
mapdl.run('poiss=0.35')
mapdl.run('densBarr=10000.0')
mapdl.run('height=10.0')
mapdl.run('width=20.0')
mapdl.run('msize=0.02')
mapdl.run('dtb=2.0	!distance to barrier')
mapdl.run('bd=1.0	!barrier depth')
mapdl.run('bw=0.2	!barrier width')
mapdl.run('nts=1000	!appr height/msize')
mapdl.run('loadhcycle=50')
mapdl.run('timestep=9.0e-6 !msize/sqrt(E/rho)')
mapdl.run('forx=1000')
mapdl.run('fory=1000')
mapdl.run('!elements')
mapdl.run('ET,1,PLANE162')
mapdl.run('KEYOPT,1,3,2')
mapdl.run('!material props')
mapdl.run('!Soil')
mapdl.run('mp,ex,1,youngSoil')
mapdl.run('mp,nuxy,1,poiss')
mapdl.run('mp,dens,1,densSoil')
mapdl.run('!Barrier')
mapdl.run('mp,ex,2,youngBarr')
mapdl.run('mp,nuxy,2,poiss')
mapdl.run('mp,dens,2,densBarr')
mapdl.run('BLC4,-width/2,-height,width,height')
mapdl.run('ESIZE,msize,0,')
mapdl.run('MSHKEY,1')
mapdl.run('mat,1')
mapdl.run('amesh,1')

cont=0

Bshape=np.loadtxt('./data.csv')
for column in range (0,15):
	for row in range (0,30):
		if Bshape[cont]==1:		
			STR='nsel,s,loc,x,dtb-msize/2+msize*2*'+str(column)+',dtb+msize/2+msize*2*('+str(column)+'+1)'
			mapdl.run(STR)
			STR='nsel,r,loc,y,-(msize/2+msize*2*('+str(row)+'+1)),-(-msize/2+msize*2*'+str(row)+')'
			mapdl.run(STR)		
			mapdl.run('ESLN,S,1')
			mapdl.run('MPCHG,2, all')
			mapdl.run('ALLSEL,ALL')
		cont=cont+1
mapdl.run('finish')
mapdl.run('/solution')
mapdl.run('NSEL,S,LOC,Y,-msize/2,msize/2')
mapdl.run('NSEL,R,LOC,X,-msize/2,msize/2')
mapdl.run('CM,LNODE,NODE')
mapdl.run('ALLSEL,ALL')
mapdl.run('*dim,etime,,4,1,1')
mapdl.run('*dim,epress,,4,1,1')
mapdl.run('*dim,epressneg,,4,1,1')
mapdl.run('etime(1)=0.0,225e-6,45e-5,1e-2')
mapdl.run('epress(1)=0,1000,0,0')
mapdl.run('epressneg(1)=0,-1000,0,0')
mapdl.run('edload,add,fx,,LNODE,etime,epress')
mapdl.run('edload,add,fy,,LNODE,etime,epressneg')
mapdl.run('edstart,0,100000000,')
mapdl.run('edcts,0,0.9')
mapdl.run('time,5e-3')
print(f'Started solving at {print_time()}')
mapdl.run('solve')
print(f'Solved at {print_time()}')
mapdl.run('FINISH')
mapdl.run('/POST26')

mapdl.nsol(nvar='2',node=str(1820),item='U',comp='Y')
mapdl.vget(par='UYZ',ir='2',tstrt='0')
mapdl.run('*VSCFUN, MINYD, MIN, UYZ')
mapdl.run('*VSCFUN, MAXYD, MAX, UYZ')
print(mapdl.parameters['MINYD'])
print(mapdl.parameters['MAXYD'])

with open('min.txt', 'w') as f:
	print(mapdl.parameters['MINYD'],file=f)
print(f'Finished simulation at {print_time()}')
