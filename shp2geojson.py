'''
Creates a geojson file from a the Shapefiles
We then apply a simplification to the polygons

Author: D.Ellis
'''

import geopandas as gpd  
import config as cf

print(vars(cf))

encoding = 'utf-8'#'ISO-8859-1'

brazil = gpd.read_file('data/shapefile/BR_borders/BR_MUN_WGS84.shp',encoding='iso-8859-1')

brazil=brazil[[type(q)!=type(None) for q in  brazil['NOME']]]

brazil['id'] = brazil['NOME']



ids = brazil.to_crs({'init':'epsg:3857'}).geometry.area.sort_values(ascending=False).index
brazil = brazil.loc[ids] 
# brazil.to_file('BR_MUN_WGS84.geojson', driver='GeoJSON')


print(brazil.loc[ids[:1000]]['id'])


'''
Simplify for Plotting
'''
print('simplifying')
import topojson as tp
topo = tp.Topology(brazil, prequantize=False)
simple = topo.toposimplify(2).to_gdf()

simple.to_file(cf.PROCESSED+'geojson/web_simplified.geojson', driver='GeoJSON', encoding=encoding)

# 
# import matplotlib.pyplot as plt
# simple.plot()
# plt.show()


# simple.geometry = simple.geometry.scale(xfact=0.9, yfact=0.9, zfact=1.0)#, origin=(0, 0))
# simple.to_file('web_simplified_2.geojson', driver='GeoJSON')

'''
iconv -f ISO-8859-1 -t UTF-8 file.php > file-utf8.php

iconv -t UTF-8 counties.geojson > counties.geojson 

'''