from ansys.mapdl import core as pymapdl
#new_path = '/home/ansys/ansys_inc/v201/ansys/bin/ansys201'
new_path = 'C:/Program Files/ANSYS Inc/v182/ansys/bin/winx64/ansys182.exe'
pymapdl.change_default_ansys_path(new_path)
import os
from ansys.mapdl.core import launch_mapdl
import datetime
import numpy as np
import time

from ...config import shape, name_conf_file

print('start'+str(datetime.datetime.now().time()))
path = os.getcwd()

mapdl=None
while mapdl is None:
	try:
		time.sleep(5)
		print(path)
		mapdl = launch_mapdl(nproc=2,run_location=path,additional_switches="-p ane3flds",mode='corba',override=True)
	except Exception as e:
		print(str(e))
		pass

mapdl.run('finish')
mapdl.run('/clear,start')
mapdl.run('/PREP7')

mapdl.run('youngSoil=30e6')
mapdl.run('poiss=0.3')
mapdl.run('densSoil=1350.0')

mapdl.run('youngBarrH=30e9')
#mapdl.run('poiss=0.35')
mapdl.run('densBarrH=2200.0')

mapdl.run('youngBarrS=30e3')
#mapdl.run('poiss=0.35')
mapdl.run('densBarrS=800.0')

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
mapdl.run('mp,ex,2,youngBarrH')
mapdl.run('mp,nuxy,2,poiss')
mapdl.run('mp,dens,2,densBarrH')
mapdl.run('mp,ex,3,youngBarrS')
mapdl.run('mp,nuxy,3,poiss')
mapdl.run('mp,dens,3,densBarrS')
mapdl.run('BLC4,-width/2,-height,width,height')
mapdl.run('ESIZE,msize,0,')
mapdl.run('MSHKEY,1')
mapdl.run('mat,1')
mapdl.run('amesh,1')

def generate_command_horizontal_vertical(horizontal_index,vertical_index):
	_command_horizontal ='nsel,r,loc,x,-(msize/2+msize*2*('+str(horizontal_index)+'+1)),-(-msize/2+msize*2*'+str(horizontal_index)+')'
	_command_vertical ='nsel,r,loc,y,-(msize/2+msize*2*('+str(vertical_index)+'+1)),-(-msize/2+msize*2*'+str(vertical_index)+')'

	return  _command_horizontal ,_command_vertical



Bshape=np.loadtxt(name_conf_file)
for vertical_y in range(shape[0]):
	for horizontal_x in range(shape[1]):
		if Bshape[vertical_y][horizontal_x]==1:		
			STR_X, STR_Y = generate_command_horizontal_vertical(horizontal_x, vertical_y)
			mapdl.run(STR_X)
			mapdl.run(STR_Y)		
			mapdl.run('ESLN,S,1')
			mapdl.run('MPCHG,2, all')
			mapdl.run('ALLSEL,ALL')
		elif Bshape[vertical_y][horizontal_x]==2:		
			STR_X, STR_Y = generate_command_horizontal_vertical(horizontal_x, vertical_y)
			mapdl.run(STR_X)
			mapdl.run(STR_Y)		
			mapdl.run('ESLN,S,1')
			mapdl.run('MPCHG,3, all')
			mapdl.run('ALLSEL,ALL')
mapdl.run('finish')
mapdl.run('/solution')
mapdl.run('NSEL,S,LOC,Y,-msize/2,msize/2')
mapdl.run('NSEL,R,LOC,X,-msize/2,msize/2')
mapdl.run('CM,LNODE,NODE')
mapdl.run('ALLSEL,ALL')
mapdl.run('*dim,etime,,4,1,1')
mapdl.run('*dim,epress,,4,1,1')
mapdl.run('*dim,epressneg,,4,1,1')
mapdl.run('etime(1)=0.0,585e-5,117e-4,26e-2')
mapdl.run('epress(1)=0,1000,0,0')
mapdl.run('epressneg(1)=0,-1000,0,0')
mapdl.run('edload,add,fx,,LNODE,etime,epress')
mapdl.run('edload,add,fy,,LNODE,etime,epressneg')
mapdl.run('edstart,0,100000000,')
mapdl.run('edcts,0,0.9')
mapdl.run('time,13e-2')
print('before solve'+str(datetime.datetime.now().time()))
mapdl.run('solve')
print('solved'+str(datetime.datetime.now().time()))
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
print('done'+str(datetime.datetime.now().time()))