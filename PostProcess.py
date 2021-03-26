''' 
A script to create movies from each file
'''

import glob, os,json 
from params import i_match,indicators
import config as cf

os.system('rm %smovies/*.webm'%cf.PROCESSED)

files = glob.glob('%splotdata/*-*_*.png'%cf.PROCESSED)

combine = {}

for ind in indicators:
    plots = list(filter(lambda x: ind in x, files))
    plots.sort()
    combine[ind] = plots

    print (len(plots))
    
    linked = '|'.join(plots)
    cmd = "ffmpeg -framerate .4 -i concat:'%s' -r 30 -c:v vp9 -pix_fmt yuva420p %smovies/%s.webm"%(linked,cf.PROCESSED,ind)

    os.system(cmd)
    
    print(cmd)
    
    
    
with open('%sallfiles.json'%cf.PROCESSED,'w') as f:
    f.write(json.dumps(combine, indent=4, sort_keys=True))
    
    