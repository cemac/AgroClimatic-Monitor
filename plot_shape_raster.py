import geopandas as gpd  
import matplotlib.pyplot as plt

import rasterio
from rasterio.plot import show
from rasterio import MemoryFile
from rasterio.mask import mask,raster_geometry_mask
from shapely.geometry import mapping

'''
Load Shapefiles
'''
brazil = gpd.read_file('./data/shapefile/BR_borders/BR_MUN_WGS84.shp')

print(brazil.columns, brazil.shape)

brazil.plot()

plt.show()


'''
Load an example tiff
'''
data = rasterio.open('data/raster/SPI/SPI06/spi_06_201901.tif')

ax = brazil.geometry.boundary.plot(edgecolor='gray',linewidth = .1,color=None)
show((data), cmap='terrain', ax=ax)
# ax.axis('off');
# plt.savefig('docs/brazil_spi&shape.png')
plt.show()


''' 
same again with contours
'''
data = rasterio.open('data/raster/SPI/SPI06/spi_06_201901.tif')

ax = brazil.geometry.boundary.plot(edgecolor='gray',linewidth = .1,color=None)
show((data), cmap='terrain', ax=ax,contour=True)
# ax.axis('off');
# plt.savefig('docs/brazil_spi&shape.png')
plt.show()


'''
last time to look at VHI
'''
data = rasterio.open('data/raster/VHI/VHI_04_2019.tif')

ax = brazil.geometry.boundary.plot(edgecolor='gray',linewidth = .1,color=None)
show((data), cmap='viridis', ax=ax)
# ax.axis('off');
# plt.savefig('docs/brazil_spi&shape.png')
plt.show()



'''
Clip tif to a single county
'''

largest = brazil.copy().to_crs({'init':'epsg:3857'}).geometry.area.sort_values().index[-1]  
rownumber = largest
selection = brazil.iloc[rownumber].geometry



clipped_array, clipped_transform = mask(data, [mapping(selection)], crop=True)

clipped = data.meta
clipped.update({"driver": "GTiff",
                     "height": clipped_array.shape[1],
                     "width": clipped_array.shape[2],
                     "transform": clipped_transform})

# -999000 is nan



with MemoryFile() as memfile:
    with memfile.open(**clipped) as dataset: # Open as DatasetWriter
        dataset.write(clipped_array)
        #del data

    dataset = memfile.open()

county=True
contour = False


ax = brazil.geometry.boundary.plot(edgecolor='red',linewidth = .3,color=None)




if contour:
    show((dataset), cmap='terrain', ax=ax, contour=True, )
else:
    show((dataset), cmap='terrain', ax=ax, contour=False,)
     # use shapefile bounds
    
plt.show()

