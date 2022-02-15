'''
CSSP Brazil

################
Main Data Script
################
Run this to create a HDF5 file for each inidicator.


indicators: VHI spi01 spi03 spi06 spi12 IIS3 RZSM

searches for tif files <apphome>/uolstorage/Data/<indicator>/<indicator>_*.tif*"

puts files <apphome>/processed/ and <apphome>/processed/plotdata/

written by d.ellis@leeds.ac.uk for CEMAC
'''
import PostProcess
from filenames_test import parsefiles
import os
import multiprocessing
#from params import indicators, iloc
from config import *
imageloc = PROCESSED + 'plotdata/'
os.system('mkdir ' + imageloc)

'''
Parse FILES
'''

'''
indicators = ['VHI','spi01','spi03','spi06','spi12','IIS3','RZSM']

iloc={
'VHI':     'VHI/VHI_*.tif',
'spi03':  'spi03/spi03_.tif',
'spi06':  'spi06/spi06_*.tif',
'spi01':  'spi01/spi01_*.tif',
'spi12':  'spi12/spi12_*.tif',
'IIS3':    'IIS3/IIS3_*.tif',
'RZSM':    'RZSM/RZSM_*.tif'
}
'''
# args from config file
args = [(kind, STORAGE + iloc[kind], PROCESSED, imageloc,)
        for kind in indicators]

# for each indicator run each_h5
for item in args:
    cmd = ' '.join(['"%s"' % i for i in item])
    os.system('python filenames_test.py ' + cmd)
