
import rasterio as rio
from rasterio.plot import show
# from rasterio.tools.mask import mask
from matplotlib import pyplot as plt
import os 

ra = rio.open("spi_03_201901.tif")
bounds  = ra.bounds
print(bounds)

# show(ra.read(), cmap='viridis')
# 
# plt.show()
my_dpi=70
plt.figure(figsize=(ra.width/my_dpi, ra.height/my_dpi), dpi=my_dpi)

ax = ax = plt.gca()
show(ra.read(1, masked=True), cmap='terrain',with_bounds=False, ax = ax)

# ax.axis('off');
# plt.savefig('docs/brazil_spi&shape.png')
plt.axis('off')
plt.tight_layout()
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig('demo.png', dpi=my_dpi, transparent=True,bbox_inches='tight',pad_inches=0)
plt.show()

os.system('convert  demo.png  -transparent white  demo2.png')