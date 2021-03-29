
import rasterio as rio
from rasterio.plot import show
import numpy as np

####################################
## rebound 
####################################
# from shapely.geometry import box
# from geopandas import GeoDataFrame
# from fiona.crs import from_epsg
# from rasterio.mask import mask
# import json
# '''
#     [-33.8689056, 5.2842873].reverse(),
#     [-73.9830625, -28.6341164].reverse()
#     [5.2842873,-33.8689056,-28.6341164,-73.9830625]
# '''
# bbox = box(-33.8689056, 5.2842873,-73.9830625, -28.6341164)
# #5.2842873,-33.8689056,-28.6341164,-73.9830625)
# geo = GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))
# # .to_crs(crs={'init': 'epsg:4326'}) # ra.crs.data
# coords = [json.loads(geo.to_json())['features'][0]['geometry']]
# img, transform = mask(dataset=ra, shapes=coords, crop=True)
# with rio.Env(projwin=-33.8689056, 5.2842873,-73.9830625, -28.6341164):
# from rasterio import Affine as A
# from rasterio.warp import reproject, Resampling
# from rasterio.tools.mask import mask


from matplotlib import pyplot as plt
import matplotlib as mpl
import os 

projection = 'EPSG:3857'
dst_crs = {'init': projection}
from rasterio.warp import reproject, Resampling



bbox = [5.2842873,-33.8689056,-35.6341164,-73.9830625]

def getpng(loc,name,what,cmap,norm,where ='./processed/plotdata/' ):
    
    if os.path.isfile('%s%s_%s.png'%(where,name,what)):
        return None
        
    plt.clf()
    
    ra = rio.open(loc)
    bounds  = ra.bounds
    # print(bounds)
    
    ratio = ra.width/ra.height



    # show(ra.read(), cmap='viridis')
    # 
    # plt.show()
    my_dpi=70
    #plt.figure(figsize=(ra.width/my_dpi, ra.height/my_dpi), dpi=my_dpi)

    width = 400
    height = int(.85 * width * ratio )
    
    
    dst_shape = (width, height)
    destination = np.zeros(dst_shape, np.uint8)
    
    reproject(
        ra,
        destination,
        # src_transform=src_transform,
        # src_crs=src_crs,
        # dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest)
    
    
    plt.figure(figsize=(width/my_dpi, height/my_dpi), dpi=my_dpi)

    ax = plt.gca()

    
    show(destination, cmap=cmap,norm=norm,with_bounds=True, ax = ax)
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
    os.system('convert %s.png -transparent white -blur 1x3 %s%s_%s.png'%(what,where,name,what))
    # -negate
    
    #print('static/plotdata/%s_%s.png'%(name,what))
    