import json,h5py
##import pandas as pd
import numpy as np


'''
Open HDF5 datafile
'''
h5file = h5py.File('../processed/data.h5', 'r')


'''
Get Data From HDH5
'''
print(list(h5file))
#what = 'spi_03']

def listfiles(what):
    return list(h5file[what])
    


def getdata(what = 'VHI', date = '01_2019'):

    selection = h5file[what][date]
    countries = list(selection) 

    data = []
    for c in countries:
        cd = selection[c].attrs
        
        data.append({'id':cd['geocode'],'name':cd['name'],'mean': float(cd['mean']),'std':float(cd['std']),'median':float(cd['median']),'min':float(cd['min']),'max':float(cd['max'])})
        
    return data 
    
    #     info = [cd['geocode'],cd['name'], cd['mean'],cd['std'],cd['median'],cd['min'],cd['max']]
    #     data.append(info)
    # 
    # df = pd.DataFrame(data,columns = 'geocode name mean std median min max'.split())
    # 
    # return df.set_index('geocode')##.to_json()
