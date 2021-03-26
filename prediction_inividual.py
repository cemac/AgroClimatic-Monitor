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
# from sktime.forecasting.theta import ThetaForecaster
# from sktime.utils.plotting import plot_series


# get_ipython().run_line_magic('matplotlib', 'inline')


# In[46]:

#min norm, abnorm, mod, sev, ext exception (else) max 8 
cat_lims = {"VHI":[[40,30,20,12,6],[100,0]],### VHI is backwards
            "spi_01":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi_03":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi_06":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi_12":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "SPI":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "RZSM":[[40,30,20,12,6],[100,0]],
            "IIS3":[[40,30,20,12,6],[100,0]]
            }


def categorize(x,idn):
    lims = cat_lims[idn]
    arr = []
    if lims[1][0]>lims[1][1]:
        for i in x:
            counter = 0
            last = True
            for j in lims[0]:
                if i > j:
                    arr.append(counter)
                    last = False
                    break
                else: 
                    counter+=1
    else:
        for i in x:
            counter = 0
            last = True
            for j in lims[0]:
                if i < j:
                    arr.append(counter)
                    last = False
                    break
                else: 
                    counter+=1

    if last: arr.append(counter)
    
    return arr,lims[1] 


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
fh = np.arange(13) #+ 1 
plot= True


def getXY(pt):
        return (pt.x, pt.y)

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

        # if np.isfinite(df).sum()>=24:
        #     shift = abs(df.min())
        # 
        #     df = pd.Series(np.nan_to_num(df, nan=0),index=df.index)
        # 
        #     forecaster = ThetaForecaster(sp=12)
        #     forecaster.fit(df+shift+1)
        #     alpha = 0.05
        #     y_pred, pred_ints = forecaster.predict(fh, return_pred_int=True, alpha=alpha)
        # 
        #     y_pred -= shift+1
        #     pred_ints["lower"] -= shift+1
        #     pred_ints["upper"] -= shift+1
        # 
        #     jsn['px'] = y_pred.index.astype('str')
        #     jsn['py'] = y_pred.values
        #     jsn['pt'] = pred_ints.upper.values
        #     jsn['pb'] = pred_ints.lower.values
        # 
        # else:
            # no predictions
            # if np.isnan(df.any()):
            #     print('failed', code, indicate)
            #     continue
            # else: 
            #     jsn['px'] = []
            #     jsn['py'] = []
            #     jsn['pt'] = []
            #     jsn['pb'] = []


        try:
            jsn['cat'],jsn['lim'] = categorize(df.values,indicate)
            jsn['catlims'] = cat_lims[indicate][0]
        except Exception as p:
            print(p,code, indicate)
            continue

        jsn['x'] = df.index.astype('str')
        jsn['y'] = df.values
        

        for i in jsn:
            jsn[i] = list(jsn[i])

        if jsn!={}:
            jsn_grp[indicate] = jsn




    # In[47]:
    b = brazil[brazil.GEOCODIGO==code]['geometry']
    x,y = b.values[0].exterior.coords.xy
    jsn_grp['geox'] = list(x)
    jsn_grp['geoy'] = list(y)
    

    jsn = {}
    yv = []
    maxl = 0
    for spi in jsn_grp:
        if 'spi_' in  spi:
            spd = jsn_grp[spi]
            jsn['x'] = spd['x']
            yv.append(spd['y'])
            # jsn['cat'] = spd['cat']
            #jsn['lim'] = spd['lim']
            jsn['catlims'] = spd['catlims']
            maxl = max(maxl,len(jsn['x']))
            
    # lazily expand array
    for i in range(len(yv)):
        for j in range(maxl-len(yv[i])):
            yv[i].append(0) 
            
            
    
    jsn['y'] = list(np.array(yv).mean(axis=0))
    jsn['cat'],jsn['lim'] = categorize(jsn['y'],indicate)
    jsn_grp['SPI'] = jsn
    
    
    jsn_grp['center'] = list(map(getXY, b.centroid))[0]

    
    json.dump(jsn_grp, open(location+'file_%s.json'%code,'w') )
    counter += 1
    print ('(%d/%d) :: '%(counter,lbr),code, 'took %.2f minutes'%((time.time()-start)/60) )

h5file.close()
print (skip)
