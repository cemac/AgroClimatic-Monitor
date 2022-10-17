"""CSSP Brazil
.. module:: dataconvert
    :platform: Unix
    :synopsis: Script for processing raster images
.. moduleauther: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This Script takes raster tifs from EPSG:4326 to EPSG:3857'.
   Map plotting requires EPSG:3857 is Pseudo-Mercator  required for plotting on
   open street maps, the EPSG:4326 format is required for all the exact lat lon
   categorising from the shape files. This is called by each_h5
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
import rasterio as rio
from rasterio.plot import show
from rasterio.crs import CRS
import rioxarray as rxr
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import os
import rasterio


# in EPSG 3857 co ords
# bbox = [y2,x2,y1,x1]
bbox = [589079.89, -3770269.33, -4250392.43, -8235756.84]
# IMPORTNAT if you get blank PNGS its likely you've put the above co ordinates
# in the wrong projection!

def getpng(loc, name, what, cmap, norm, where='./processed/plotdata/'):

    if os.path.isfile('%s%s_%s.png' % (where, name, what)):
        print('png already exists skipping ', where, ' ', name,' ', what)
        return None  # exists

    plt.cla()
    # Open street maps are in EPSG:3857 so either take pngs
    try:
        ra=rxr.open_rasterio(loc, masked=True).squeeze()
        # check projection
        projection = str(ra.rio.crs)
        if projection == 'EPSG:4326':
            print('reprojecting from 4326 to EPSG:3857')
            crs_wgs84 = CRS.from_string('EPSG:4326')
            # reproject to EPSG:4326
            ra = ra.rio.reproject(crs_wgs84)
            ra.rio.to_raster('./temp.tif')
            data = rasterio.open('./temp.tif')
            os.system('rm ./temp.tif')
        else:
            data = rasterio.open(loc)
    except ValueError:
        # A weird error is worked around by not decoding the times or mask
        'Strang Mask or time values'
        ra=rxr.open_rasterio(loc, decode_times=False).squeeze()
        # check projection
        projection = str(ra.rio.crs)
        if projection == 'EPSG:4326':
            print('reprojecting from EPSG:4326 to EPSG:3857')
            crs_wgs84 = CRS.from_string('EPSG:3857')
            # reproject to EPSG:4326
            ra = ra.rio.reproject(crs_wgs84)
            ra.rio.to_raster('./temp.tif')
            data = rasterio.open('./temp.tif')
            os.system('rm ./temp.tif')
        else:
            data = rasterio.open(loc)


    try:
        ra = rxr.open_rasterio(loc,masked=True).squeeze()
    except ValueError:
        ra = rxr.open_rasterio(loc, decode_times=False).squeeze()

    bounds = ra.rio.bounds
    ratio = ra.rio.width / ra.rio.height
    my_dpi = 70
    width = 400
    height = int(.85 * width * ratio)
    plt.figure(figsize=(width / my_dpi, height / my_dpi), dpi=70)
    ax=plt.gca()
    plt.axis('off')
    show(data, cmap=cmap, norm=norm, with_bounds=True,ax=ax)
    plt.xlim(bbox[-1], bbox[1])
    plt.ylim(bbox[-2], bbox[0])
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.text(.95, .95, '-'.join(name.split('-')[::-1]), horizontalalignment='center',
             verticalalignment='center', transform=ax.transAxes, c='black')
    print('FILENAME ', what)
    plt.savefig('%s.png' % what, dpi=70,
                transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
    # blur and invert
    # remove -blur 1x3
    os.system('convert %s.png -transparent whitesmoke %s%s_%s.png' %
              (what, where, name, what))
