"""CSSP Brazil
.. module::
    :platform: Unix
    :synopsis: config file
.. moduleauther: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This file is a simple configuation file defining variables used
   accross multiple scripts
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""

indicators = ['VHI','spi01','spi03','spi06','spi12','IIS3','RZSM']

i_match = 'VHI spi IIS3 RZSM'.split()


dkeys = [
    "",
    "Normal",
    "Abnormally Dry",
    "Moderate Drought",
    "Severe Drought",
    "Extreme Drought",
    "Exceptional Drought",
    ""];
dnames = [
    "",
    "Normal",
    "Dry",
    "Moderate",
    "Severe",
    "Extreme",
    "Exceptional",
    ""];


cat_lims = {"VHI":[[40,30,20,12,6],[100,0]],### VHI is backwards
            "spi01":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi03":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi06":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi12":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "SPI":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "RZSM":[[30,20,11,6,3],[100,0]],
            "IIS3":[[6,5,4,3,2],[7,0]]
            }


colours = 'whitesmoke whitesmoke #FFFFCC #FED976 #FD8C3C #E2191C #800026'.split()[::-1]


print('CHANGE PARAM LOCATION')

iloc={
'VHI':    'VHI/VHI_*.tif',
'spi03':  'spi03/spi03_*.tif',
'spi06':  'spi06/spi06_*.tif',
'spi01':  'spi01/spi01_*.tif',
'spi12':  'spi12/spi12_*.tif',
'IIS3':   'IIS3/IIS3_*.tif',
'RZSM':   'RZSM/RZSM_*.tif'
}
