'''
Process individual hdf5 FILES

CSSP brazil
written by d.ellis@leeds.ac.uk for CEMAC
'''

import geopandas as gpd
import rasterio
import h5py
import glob
import time
from rasterio import MemoryFile
from rasterio.crs import CRS
import rioxarray as rxr
from rasterio.mask import mask, raster_geometry_mask
from shapely.geometry import mapping
from numpy import ma, nan, where, nanmean, nanstd, nanmedian, nanmax, nanmin, isfinite
from matplotlib import pyplot as plt
import matplotlib as mpl
import os
import warnings
import sys
import dataconvert as dc
import config as cf
from params import cat_lims, colours
warnings.filterwarnings('ignore', category=RuntimeWarning)
'''
Load Shapefiles
'''
brazil = gpd.read_file(cf.DATA + 'shapefile/BR_borders/BR_MUN_WGS84.shp')
# To get raster in lat lon we need this projection
req_projection = 'EPSG:4326'
# Other projection can be dealt with e.g.: EPSG:3857
# Main parsefiles Function

def parsefiles(i_kind, FILES, dataloc, imageloc):
    '''
    ----------------------------------------
    Indicator Function
    ----------------------------------------
    i_kind :: str - indicator type
    indicator_files :: list - filelocations
    dataloc :: str - data Location
    imageloc :: str - image location for saving
    '''
    print('i_kind: ', i_kind)
    print(' FILES: ', FILES)
    print('dataloc: ', dataloc)
    print('imageloc', imageloc)
    thisfile = '%sdata_%s.h5' % (dataloc, i_kind)
    print('thisfile: ', thisfile)
    # How many tif files present in <STORAGE>/Data/<inidicator>/
    FILES = glob.glob(FILES)
    nfiles = len(FILES)
    print('Number of %s files' % i_kind, nfiles)
    # - <index_name>_YYYY_MM.tif (where <index_name> can take: IIS3, RZSM, SPI01, SPI03, SPI06 and SPI12)

    # Create h5 file and pngs
    for counter, f in enumerate(FILES):
        # f = path/index_name>_YYYY_MM.tif
        # get file name <index_name>_YYYY_MM.tif
        # buy splitting at / and removing file extenstion
        fname = f.split('/')[-1].replace('.tif', '')
        # Now split into three <index>,<yyyy>,<mm>
        fname = fname.split('_')
        fname = '%s-%s' % (fname[1], fname[2])
        print(i_kind + ' : ' + fname)
        # perform some checks


    return i_kind + ' finished'


if __name__ == '__main__':
    #     print(sys.argv)
    parsefiles(*sys.argv[1:5])
