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
    #check if h5 exists and if
    if os.path.exists(thisfile):
        basetime = os.path.getmtime(thisfile)
        print('file exists and basetime: ', basetime)
    else:
        basetime = -0

    try:
        indicator = h5py.File(thisfile, 'a')
        print('indicator: ', indicator)

    except:
        # try closing all instances of the file first
        basetime = -1
        print('deleting: ', thisfile)
        os.system('rm ' + thisfile)
        # input('deleting ctrl-c to cancel, enter to continue')
        # h5file = h5py.File( datafile, 'w')
        print('FAILED retrying')
        indicator = h5py.File(thisfile, 'a')

    # How many tif files present in <STORAGE>/Data/<inidicator>/
    FILES = glob.glob(FILES)
    nfiles = len(FILES)
    print('Number of %s files' % i_kind, nfiles)
    # - <index_name>_YYYY_MM.tif (where <index_name> can take: IIS3, RZSM, SPI01, SPI03, SPI06 and SPI12)

    # Create h5 file and pngs
    for counter, f in enumerate(FILES):
        # get file name <index_name>_YYYY_MM.tif
        fname = f.split('/')[-1].replace('.tiff',
                                         '').replace('.tif', '').replace(i_kind + '_', '')
        if i_kind == 'VHI' or i_kind == 'IIS3':
            fname = fname.split('_')
            fname = '%s-%s' % (fname[1], fname[0])
        elif i_kind == 'RZSM':
            fname = fname.split('_')
            fname = '%s-%s' % (fname[0], fname[1])
        else:
            fname = '%s-%s' % (fname[0:4], fname[4:])
        print(fname)


    return i_kind + ' finished'


if __name__ == '__main__':
    #     print(sys.argv)
    parsefiles(*sys.argv[1:5])
