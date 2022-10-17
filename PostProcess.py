"""CSSP Brazil
.. module:: PostProcess
    :platform: Unix
    :synopsis: Batch Script for processing muncipalities
.. moduleauther: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This Script called by each_h5 and creates movies from all the pngs
   that have been generated
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
'''
A script to create movies from each file
'''

import glob, os,json
from params import i_match,indicators
import config as cf


def update():

    os.system('rm %smovies/*.webm'%cf.PROCESSED)

    files = glob.glob('%splotdata/*-*_*.png'%cf.PROCESSED)

    combine = {}

    for ind in indicators:
        plots = list(filter(lambda x: ind in x, files))
        plots.sort()

        print(plots,ind)
        print (len(plots))

        linked = '|'.join(plots)
        cmd = "ffmpeg -framerate .4 -i concat:'%s' -r 30 -c:v vp9 -pix_fmt yuva420p %smovies/%s.webm"%(linked,cf.PROCESSED,ind)

        os.system(cmd)

        combine[ind] = [i.split('/plotdata/')[1] for i in plots]
        #only take filenames

        print(cmd)




    with open('%sallfiles.json'%cf.PROCESSED,'w') as f:
        f.write(json.dumps(combine, indent=4, sort_keys=True))

    return plots

if __name__ == '__main__':
    out = update()
