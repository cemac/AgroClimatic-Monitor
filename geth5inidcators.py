import json,h5py,time
##import pandas as pd
import numpy as np
import geopandas as gpd

'''
Open HDF5 datafile
'''
h5file = h5py.File('./processed/data.h5', 'r')

# indicatiors = h5py.File('../processed/indicators.h5', 'a')

brazil = gpd.read_file('./data/shapefile/BR_borders/BR_MUN_WGS84.shp').GEOCODIGO.sort_values()

def vhi_val(x):
    if    x>40.: return -1
    elif  x>30.: return 0
    elif  x>20.: return 1
    elif  x>12.: return 2
    elif  x>6. : return 3
    else       : return 4
    
def spi_val(x):    
    if    x>-.5 : return -1
    elif  x>-.8 : return 0
    elif  x>-1.3: return 1
    elif  x>-1.6: return 2
    elif  x>-2.0: return 3
    else       : return 4

miss=[]
skip = ['2605459', '4300001', '4300002']








data = {}

vhi = h5file['VHI']
sp3 = h5file['spi_03']
sp6 = h5file['spi_06']



start = time.time()

for i in vhi:
    data[i] = {}
    for j in brazil:
        if j in skip:continue
        data[i][j] =  {}#{'vhi':None,'spi_03':None,'spi_06':None}
        try:
            data[i][j]['vhi'] = vhi_val(vhi[i][j].attrs['median'])
            data[i][j]['spi3'] = spi_val(sp3[i][j].attrs['median'])
            data[i][j]['spi6'] = spi_val(sp6[i][j].attrs['median'])
        except Exception as e:
            print(e)
            miss.append(j)
        
print((time.time()-start)/60,'minutes')


with open('./serverapp/templates/static/biindicate.json','w') as f:
    f.write(json.dumps(data).replace(' ',''))
    
    
    