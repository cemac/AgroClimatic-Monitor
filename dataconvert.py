import rasterio as rio
from rasterio.plot import show
from rasterio.warp import reproject, Resampling
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import os

def getpng(loc, name, what, cmap, norm, where='./processed/plotdata/'):

    #if os.path.isfile('%s%s_%s.png' % (where, name, what)):
    #    return None  # exists

    plt.cla()
    ra = rio.open(loc)
    bounds = ra.bounds
    ratio = ra.width / ra.height
    my_dpi = 70
    width = 400
    height = int(.85 * width * ratio)
    plt.figure(figsize=(width / my_dpi, height / my_dpi), dpi=70)
    ax=plt.gca()
    plt.axis('off')
    show(ra, cmap=cmap, norm=norm, with_bounds=True,ax=ax)
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.text(.95, .95, '-'.join(name.split('-')[::-1]), horizontalalignment='center',
             verticalalignment='center', transform=ax.transAxes, c='black')
    print('FILENAME ', what)
    plt.savefig('%s.png' % what, dpi=70,
                transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
    # blur and invert
    # remove -blur 1x3
    os.system('convert %s.png -transparent whitesmoke %s%s_%s.png' %
              (what, where, name, what))
