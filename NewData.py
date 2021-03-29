'''
CSSP Brazil 

################
Main Data Script
################
Run this to create a HDF5 file for each inidicator.


written by d.ellis@leeds.ac.uk for CEMAC
'''

dataloc = './processed/'
imageloc = './processed/plotdata/'



'''
Locate Data
'''





from each_h5 import parsefiles  
import os, multiprocessing
from params import indicators,iloc


''' 
Parse FILES
'''
#


## overwrite
# indicators = 'VHI RZSM'.split()


args = [(kind,iloc[kind],dataloc,imageloc,) for kind in indicators]


print('### this should be done in a batch script!')
for item in args:
    cmd = ' '.join(['"%s"'%i for i in item])
    print(cmd)
    os.system('python each_h5.py '+cmd)




### movies
import PostProcess
PostProcess.update()

print ('ALL UP TO DATE')
# clean up
os.system('rm *_*.png')
