
import rasterio as rio
from rasterio.plot import show
from rasterio.warp import reproject, Resampling

import numpy as np

from matplotlib import pyplot as plt
import matplotlib as mpl
import os 

projection = 'EPSG:3857'
input_proj = 'EPSG:4326'


bbox = [5.2842873,-33.8689056,-35.6341164,-73.9830625]

def getpng(loc,name,what,cmap,norm,where ='./processed/plotdata/' ):
    
    if os.path.isfile('%s%s_%s.png'%(where,name,what)): return None # exists
        
    plt.clf()
    
    ra = rio.open(loc)
    bounds  = ra.bounds

    ratio = ra.width/ra.height

    # show(ra.read(), cmap='viridis')
    # plt.show()
    my_dpi=70
    #plt.figure(figsize=(ra.width/my_dpi, ra.height/my_dpi), dpi=my_dpi)

    width = 400
    height = int(.85 * width * ratio )
    
    
    dst_shape = (width, height)
    #destination = np.zeros(dst_shape, np.uint8)
    
    
    dst = rio.open('./temp.tiff','w')
    reproject(
        rio.band(ra,1),
        rio.band(destination,1),
        # src_transform=src_transform,
        src_crs={'init': input_proj},
        # dst_transform=dst_transform,
        dst_crs={'init': projection},
        resampling=Resampling.nearest)
    # 
    
    plt.figure(figsize=(width/my_dpi, height/my_dpi), dpi=my_dpi)

    ax = plt.gca()

    
    show(ra, cmap=cmap,norm=norm,with_bounds=True, ax = ax)
    #ra.read(1, masked=True)
    # 
    plt.xlim(bbox[-1],bbox[1])
    plt.ylim(bbox[-2],bbox[0])
    
    plt.axis('off')
    plt.tight_layout()
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    plt.text(.95,.95, '-'.join(name.split('-')[::-1]), horizontalalignment='center',          verticalalignment='center', transform=ax.transAxes, c='black')

    
    plt.savefig('%s.png'%what, dpi=my_dpi, transparent=True,bbox_inches='tight',pad_inches=0)
    #plt.show()
    plt.close()

    # blur and invert
    os.system('convert %s.png -transparent whitesmoke -blur 1x3 %s%s_%s.png'%(what,where,name,what))
