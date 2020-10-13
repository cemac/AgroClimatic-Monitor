'''
Creates a geojson file from a the Shapefiles
'''

import geopandas as gpd  

brazil = gpd.read_file('./shapefile/BR_borders/BR_MUN_WGS84.shp')
brazil['id'] = brazil['NOME']
ids = brazil.to_crs({'init':'epsg:3857'}).geometry.area.sort_values(ascending=False).index
brazil = brazil.loc[ids] 
brazil.to_file('BR_MUN_WGS84.geojson', driver='GeoJSON')



'''
Simplify for Plotting
'''
print('simplifying')
import topojson as tp
topo = tp.Topology(brazil, prequantize=False)
simple = topo.toposimplify(10).to_gdf()

simple.to_file('web_simplified.geojson', driver='GeoJSON')

# 
# import matplotlib.pyplot as plt
# simple.plot()
# plt.show()


simple.geometry = simple.geometry.scale(xfact=0.9, yfact=0.9, zfact=1.0)#, origin=(0, 0))
simple.to_file('web_simplified_2.geojson', driver='GeoJSON')