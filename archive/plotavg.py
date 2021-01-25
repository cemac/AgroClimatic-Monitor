import json,h5py
import pandas as pd
import numpy as np
'''
Open HDF5 datafile
'''
h5file = h5py.File('processed/data.h5', 'r')

# 
# from urllib.request import urlopen
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     demo = json.load(response)

counties = json.load(open('data/BR_MUN_WGS84.geojson'))

# 
# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
#                    dtype={"fips": str})



'''
Get Data From HDH5
'''
print(list(h5file))
what = 'spi_03'

dates = list(h5file[what])
selection = h5file[what][dates[-1]]
countries = list(selection) 

data = []
for c in countries:
    cd = selection[c].attrs
    info = [cd['geocode'],c, cd['mean'],cd['std'],cd['median'],cd['min'],cd['max']]
    data.append(info)

df = pd.DataFrame(data,columns = 'geocode name mean std median min max'.split())

df.to_csv('processed/vhi_group.csv')
print(df.head)

# 
# '''
# Plotting
# '''
# import plotly.express as px
# 
# 
# fig = px.choropleth(df, geojson=counties, locations='name', color='median',
#                            color_continuous_scale="Viridis",
#                            range_color=(np.min(df['min']), np.max(df['max'])),
#                            scope="south america",
#                            labels={what:'index'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
# 
# 
# 
# 
# print('fi','http://127.0.0.1:50371')
# 
# 



'''

https://github.com/plotly/dash-opioid-epidemic-demo
       fips  unemp
0     01001    5.3
1     01003    5.4
2     01005    8.6

'''