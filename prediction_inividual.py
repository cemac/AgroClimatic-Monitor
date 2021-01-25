#!/usr/bin/env python
# coding: utf-8

# In[1]:


from warnings import simplefilter
simplefilter("ignore", FutureWarning)
import numpy as np
import pandas as pd
import h5py,json,time
import geopandas as gpd
# from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.theta import ThetaForecaster
# from sktime.utils.plotting import plot_series


# get_ipython().run_line_magic('matplotlib', 'inline')


# In[46]:


'''
Open HDF5 datafile
'''

h5file = h5py.File('./processed/newdata.h5', 'r')
brazil = gpd.read_file('./data/shapefile/BR_borders/BR_MUN_WGS84.shp')
codenames = brazil.GEOCODIGO.sort_values().values.astype(str)
lbr = len(codenames)


location = './processed/muncipalities/'



indicators = list(h5file)
item = 'mean'
fh = np.arange(12) + 1 
plot= True

# code = np.random.choice(codenames)
# indicate = np.random.choice(indicators)
# print(code,indicate)
# list(h5file[indicate])
# code='1100049'

print(indicators)

counter = 0
# In[48]:
skip = []
print('starting loop')
for code in codenames:
    start = time.time()
    jsn_grp={}
    for indicate in indicators:

        jsn={}
        try:
            selection = h5file[indicate][code]
            dtstr = [i+'-01 00:00:00' for i in selection]
        except: 
            skip.append([code,indicate])
            continue

        
        
        df = pd.Series([selection[i].attrs[item] for i in selection],
                         index = pd.to_datetime(dtstr).to_period('M')
                      )
        # we cant deal with negative values, so shift the results up
        
        if np.isfinite(df).sum()>=24:
            shift = abs(df.min())
            

            forecaster = ThetaForecaster(sp=12)
            forecaster.fit(df+shift+1)
            alpha = 0.05
            y_pred, pred_ints = forecaster.predict(fh, return_pred_int=True, alpha=alpha)

            y_pred -= shift+1
            pred_ints["lower"] -= shift+1
            pred_ints["upper"] -= shift+1
            
            jsn['px'] = y_pred.index.astype('str')
            jsn['py'] = y_pred.values
            jsn['pt'] = pred_ints.upper.values
            jsn['pb'] = pred_ints.lower.values
            
        else:
            # no predictions
            jsn['px'] = []
            jsn['py'] = []
            jsn['pt'] = []
            jsn['pb'] = []

        jsn['x'] = df.index.astype('str')
        jsn['y'] = df.values
        

        for i in jsn:
            jsn[i] = list(jsn[i])

        jsn_grp[indicate] = jsn

    # In[47]:
    x,y = brazil[brazil.GEOCODIGO==code]['geometry'].values[0].exterior.coords.xy
    jsn['geox'] = list(x)
    jsn['geoy'] = list(y) 
    
    json.dump(jsn_grp, open(location+'file_%s.json'%code,'w') )
    counter += 1
    print ('(%d/%d) :: '%(counter,lbr),code, 'took %.2f minutes'%((time.time()-start)/60) )

h5file.close()
print (skip)
