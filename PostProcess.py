import glob, os,json 
from params import i_match,indicators

os.system('rm ./processed/movies/*.webm')

files = glob.glob('./processed/plotdata/*-*_*.png')

combine = {}

for ind in indicators:
    plots = list(filter(lambda x: ind in x, files))
    plots.sort()
    combine[ind] = plots

    print (len(plots))
    
    linked = '|'.join(plots)
    cmd = "ffmpeg -framerate .4 -i concat:'%s' -r 30 -c:v vp9 -pix_fmt yuva420p ./processed/movies/%s.webm"%(linked,ind)

    os.system(cmd)
    
    print(cmd)
    
    
    
with open('./processed/allfiles.json','w') as f:
    f.write(json.dumps(combine, indent=4, sort_keys=True))
    
    