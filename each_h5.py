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
    '''
    CBAR

    create a colour bar to create the pngs for data browser and movies
    '''
    print('creating colourbar')
    cat = cat_lims[i_kind]
    bins = [cat[1][0]]
    bins.extend(cat[0])
    bins.append(cat[1][1])
    col = colours
    if bins[-1] < bins[0]:
        print('REVERSEcolour', i_kind)
        bins = bins[::-1]
        cols = colours[::-1]
    cmap = mpl.colors.ListedColormap(col)
    norm = mpl.colors.BoundaryNorm(
        boundaries=bins, ncolors=len(cmap.colors) - 1)
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)
    cb2 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                    norm=norm,
                                    boundaries=bins,
                                    extend='both',
                                    ticks=bins,
                                    spacing='proportional',
                                    orientation='horizontal')
    cb2.set_label(i_kind)
    plt.savefig(imageloc + i_kind + '.png',  transparent=True, bbox_inches='tight',
                pad_inches=0)

    # Create h5 file and pngs
    for counter, f in enumerate(FILES):
        start = time.time()
        '''
        Iterate over each county for each file
        - less IO overhead this way
        '''
        # if tiff file is older than h5 file then skip
        # if basetime>os.path.getmtime(f):
        #    print('Skipping:',f ,basetime, os.path.getmtime(f) )
        #    continue # this file is older than the combigned one - ignore.
        #data = rasterio.open(f)
        try:
            ra=rxr.open_rasterio(f, masked=True).squeeze()
            # check projection
            projection = str(ra.rio.crs)
            if projection == 'EPSG:3857':
                print('reprojecting from EPSG:3857 to EPSG:4326')
                crs_wgs84 = CRS.from_string('EPSG:4326')
                # reproject to EPSG:4326
                ra = ra.rio.reproject(crs_wgs84)
                ra.rio.to_raster('./temp.tif')
                data = rasterio.open('./temp.tif')
                os.system('rm ./temp.tif')
            else:
                data = rasterio.open(f)
        except ValueError:
            'Strang Mask or time values'
            ra=rxr.open_rasterio(f, decode_times=False).squeeze()
            # check projection
            projection = str(ra.rio.crs)
            if projection == 'EPSG:3857':
                print('reprojecting from EPSG:3857 to EPSG:4326')
                crs_wgs84 = CRS.from_string('EPSG:4326')
                # reproject to EPSG:4326
                ra = ra.rio.reproject(crs_wgs84)
                ra.rio.to_raster('./temp.tif')
                data = rasterio.open('./temp.tif')
                os.system('rm ./temp.tif')
            else:
                data = rasterio.open(f)

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

        ###
        # Generate pngs used in data browser
        ###
        #  getpng(loc, name, what, cmap, norm, where='./processed/plotdata/')

        dc.getpng(f, fname, i_kind, cmap, norm, imageloc)
        
        for shape in brazil.iterrows():
            # polygon shapes
            selection = shape[1].geometry
            # ID
            sname = str(shape[1].GEOCODIGO)
            # humand readable name
            name = shape[1].NOME
            if not name:
                continue

            '''## subgroup'''
            try:
                indicator_sub = indicator[sname]
            except KeyError:
                indicator_sub = indicator.create_group(sname)

            # clip
            try:
                clipped_array, clipped_transform = mask(
                    data, [mapping(selection)], crop=True)
            except ValueError:
                continue

            # MASK based on max limit
            if i_kind != 'IIS3':
                masked = where(clipped_array <=
                               data.meta['nodata'], nan, clipped_array)
            else:
                masked = where(clipped_array >=
                               data.meta['nodata'], nan, clipped_array)

            # try: nanmax(masked)
            # except RuntimeWarning: continue
            if not isfinite(masked.any()):
                continue

            '''## save data'''
            try:
                dset = indicator_sub[fname]
            except KeyError:

                # create dataset
                dset = indicator_sub.create_dataset(
                    fname, masked.shape, dtype='float32')
                dset[:] = masked
                dset.attrs['transform'] = clipped_transform
                dset.attrs['geocode'] = shape[1].GEOCODIGO
                dset.attrs['name'] = name

                # dataset
                dset.attrs['max'] = nanmax(masked)
                dset.attrs['min'] = nanmin(masked)
                dset.attrs['median'] = nanmedian(masked)
                dset.attrs['mean'] = nanmean(masked)
                dset.attrs['std'] = nanstd(masked)
                #
                # print('----',dset.attrs['min'],dset.attrs['max'])
        print('(%d/%d) :: ' % (counter + 1, nfiles), fname,
              'took %.2f minutes' % ((time.time() - start) / 60))

    '''
    Close the hdf5 file cleanly
    '''
    indicator.close()
    return i_kind + ' finished'


if __name__ == '__main__':
    #     print(sys.argv)
    parsefiles(*sys.argv[1:5])
