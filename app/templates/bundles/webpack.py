'''
Compile the website

npm -ig webpack
needs to be installed globally
'''

import os , sys

cmd = 'webpack --entry=./index.js --output-filename=./bundle.js --mode=production'

import glob
loc = __file__.replace('webpack.py','')
# if loc=='':loc = './'
print('App Location:', loc)

try:
    assert len(sys.argv)>1
    files = ['%s%s/dist'%(i,loc) for i in sys.argv[1:]]
except:
    ## from all directories with a dist folder
    files = glob.glob('%s*/dist'%loc)
    # print(files)




for f in files:
    f = f.replace('/dist','')
    r = os.popen('cd %s && NODE_PATH=/var/www/miniconda3/envs/agro-python/lib/node_modules %s'%(f,cmd)).read()
    if 'error' not in r and 'such' not in r:
        print('web packed', f ,'\n')
    else:
        print('ERROR',f,r)
        print('ERROR',f,'\n')
