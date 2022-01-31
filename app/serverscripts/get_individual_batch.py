#!/usr/bin/env python
# coding: utf-8

import time
import json
import h5py
from serverscripts.config import *
import pandas as pd
import numpy as np
from warnings import simplefilter
simplefilter("ignore", FutureWarning)
# min norm, abnorm, mod, sev, ext exception (else) max 8
cat_lims = {"VHI": [[40, 30, 20, 12, 6], [100, 0]],  # VHI is backwards
            "spi_01": [[-.5, -.8, -1.3, -1.6, -2], [4, -4]],
            "spi_03": [[-.5, -.8, -1.3, -1.6, -2], [4, -4]],
            "spi_06": [[-.5, -.8, -1.3, -1.6, -2], [4, -4]],
            "spi_12": [[-.5, -.8, -1.3, -1.6, -2], [4, -4]],
            "SPI": [[-.5, -.8, -1.3, -1.6, -2], [4, -4]],
            "RZSM": [[40, 30, 20, 12, 6], [100, 0]],
            "IIS3": [[6, 5, 4, 3, 2], [7, 0]]
            }

location = PROCESSED + 'muncipalities_batch/'

polydata = pd.read_csv(PROCESSED + 'geojson/poly.csv')
polydata.GEOCODIGO = polydata.GEOCODIGO.astype(str)


def categorize(x, idn):
    lims = cat_lims[idn]
    arr = []
    last = False
    if lims[1][0] > lims[1][1]:
        for i in x:
            counter = 0
            last = True
            for j in lims[0]:
                if i > j:
                    arr.append(counter)
                    last = False
                    break
                else:
                    counter += 1
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
                    counter += 1

    if last:
        arr.append(counter)

    return arr, lims[1]


'''
Open HDF5 datafile
'''


def m_new(code):

    # code = code.replace('file_','').replace('.json')
    global polydata
    print(polydata.GEOCODIGO.values, code, '\n\n\n\n\n\n\n\n')
    start = time.time()
    jsn_grp = {}
    for hf in h5locs:
        indicate = hf.replace(PROCESSED + 'data_', '').replace('.h5', '')
        h5file = h5py.File(hf, 'r')
        jsn = {}
        try:
            selection = h5file[code]
            dtstr = [i + '-01 00:00:00' for i in selection]
        except Exception as e:
            print(e)
            print('failure')
            continue

        df = pd.Series([selection[i].attrs['median'] for i in selection],
                       index=pd.to_datetime(dtstr).to_period('M')
                       )
        df.dropna(inplace=True)
        try:
            jsn['cat'], jsn['lim'] = categorize(df.values, indicate)
            jsn['catlims'] = cat_lims[indicate][0]
        except Exception as p:
            print('error')
            print(p, code, indicate)
            continue

        jsn['x'] = df.index.astype('str')
        jsn['y'] = df.values

        for i in jsn:
            jsn[i] = list(jsn[i])

        if jsn != {}:
            jsn_grp[indicate] = jsn

        h5file.close()

    it = polydata[polydata.GEOCODIGO == code]

    poly = eval(it.poly.values[0])

    jsn_grp['geox'] = poly[0]
    jsn_grp['geoy'] = poly[1]
    jsn_grp['micro'] = it['MICROREGIA'].values[0]
    jsn_grp['macro'] = it['MESOREGIAO'].values[0]
    jsn_grp['id'] = it['id'].values[0]
    jsn = {}
    yv = []
    maxl = 0
    for spi in jsn_grp:
        if 'spi_' in spi:
            spd = jsn_grp[spi]
            jsn['x'] = spd['x']
            yv.append(spd['y'])
            # jsn['cat'] = spd['cat']
            #jsn['lim'] = spd['lim']
            jsn['catlims'] = spd['catlims']
            maxl = max(maxl, len(jsn['x']))
    # lazily expand array
    for i in range(len(yv)):
        for j in range(maxl - len(yv[i])):
            yv[i].append(0)

    if len(yv) > 0:
        jsn['y'] = list(np.array(yv).mean(axis=0))
        jsn['cat'], jsn['lim'] = categorize(jsn['y'], indicate)
    else:
        jsn = {}

    jsn_grp['SPI'] = jsn
    json.dump(str(jsn_grp), open(location + 'file_%s.json' % code, 'w'))
    print(time.time() - start)
    return jsn_grp
