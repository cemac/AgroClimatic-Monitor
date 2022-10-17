"""CSSP Brazil
.. module:: NewData
    :platform: Unix
    :synopsis: Batch Script for processing muncipalities
.. moduleauther: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This Script is called to handle new data in the upload folder passing
   to each_h5.py the storage location for the indicator, the indicaor and where
   to put the processed files
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
Example:
    To use::
        python app.py
        It is best to run this app via a web server gunicorn or Apache
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
'''
CSSP Brazil

################
Main Data Script
################
Run this to create a HDF5 file for each inidicator.


indicators: VHI spi_01 spi_03 spi_06 spi_12 IIS3 RZSM

searches for tif files <apphome>/uolstorage/Data/<indicator>/<indicator>_*.tif*"

puts files <apphome>/processed/ and <apphome>/processed/plotdata/

written by d.ellis@leeds.ac.uk for CEMAC
'''
import PostProcess
from each_h5 import parsefiles
import os
import multiprocessing
from params import indicators, iloc
from config import *
imageloc = PROCESSED + 'plotdata/'
os.system('mkdir ' + imageloc)

'''
Parse FILES
'''
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
