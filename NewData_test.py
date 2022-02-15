'''
CSSP Brazil

################
Main Data Script
################
Run this to create a HDF5 file for each inidicator.


indicators: VHI SPI01 SPI03 SPI06 SPI12 IIS3 RZSM

searches for tif files <apphome>/uolstorage/Data/<indicator>/<indicator>_*.tif*"

puts files <apphome>/processed/ and <apphome>/processed/plotdata/

written by d.ellis@leeds.ac.uk for CEMAC
'''
import PostProcess
from each_h5 import parsefiles
import os
import multiprocessing
#from params import indicators, iloc
from config import *
imageloc = PROCESSED + 'plotdata/'
os.system('mkdir ' + imageloc)

'''
Parse FILES
'''

Test new indicators and ilocs
indicators = ['VHI','SPI01','SPI03','SPI06','SPI12','IIS3','RZSM']

iloc={
'VHI':     'VHI/VHI_*.tif',
'SPI03':  'SPI03/SPI03_.tif',
'SPI06':  'SPI06/SPI06_*.tif',
'SPI01':  'SPI01/SPI01_*.tif',
'SPI12':  'SPI12/SPI12_*.tif',
'IIS3':    'IIS3/IIS3_*.tif',
'RZSM':    'RZSM/RZSM_*.tif'
}
# args from config file
args = [(kind, STORAGE + iloc[kind], PROCESSED, imageloc,)
        for kind in indicators]

# for each indicator run each_h5
for item in args:
    cmd = ' '.join(['"%s"' % i for i in item])
    os.system('python each_h5.py ' + cmd)

# movies
PostProcess.update()

print('ALL UP TO DATE')
# clean up
os.system('rm *_*.png')
