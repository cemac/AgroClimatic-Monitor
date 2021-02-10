
import rasterio as rio
from rasterio.plot import show
# from rasterio.tools.mask import mask
from matplotlib import pyplot as plt
import matplotlib as mpl
import os 


def getpng(loc,name,what,cmap,norm,where ='./processed/plotdata/' ):
    
    if os.path.isfile('%s%s_%s.png'%(where,name,what)):
        return None
        
    plt.clf()
    
    ra = rio.open(loc)
    bounds  = ra.bounds
    # print(bounds)
    
    ratio = ra.width/ra.height


    # show(ra.read(), cmap='viridis')
    # 
    # plt.show()
    my_dpi=70
    #plt.figure(figsize=(ra.width/my_dpi, ra.height/my_dpi), dpi=my_dpi)

    width = 300
    height = width * ratio
    
    plt.figure(figsize=(width/my_dpi, height/my_dpi), dpi=my_dpi)

    ax = plt.gca()
    show(ra.read(1, masked=True), cmap=cmap,
                                    norm=norm,with_bounds=False, ax = ax)

    plt.axis('off')
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    plt.text(0, 0, name, horizontalalignment='center',          verticalalignment='center', transform=ax.transAxes, c='white')

    
    plt.savefig('demo.png', dpi=my_dpi, transparent=True,bbox_inches='tight',pad_inches=0)
    #plt.show()
    plt.close()

    # blur and invert
    os.system('convert demo.png -transparent white -blur 0x1 %s%s_%s.png'%(where,name,what))
    # -negate
    
    #print('static/plotdata/%s_%s.png'%(name,what))
    