import geopandas as gpd  
import rasterio,h5py,glob,time
from rasterio import MemoryFile
from rasterio.mask import mask,raster_geometry_mask
from shapely.geometry import mapping
import dataconvert as dc

from numpy import ma,nan,where,nanmean,nanstd,nanmedian,nanmax,nanmin,isfinite
import os,warnings

warnings.filterwarnings('ignore', category=RuntimeWarning)
'''
Open HDF5 datafile
'''

datafile = 'processed/newdata.h5'
imageloc = './processed/plotdata/'



try:
    h5file = h5py.File( datafile , 'a')
except:
        # try closing all instances of the file first
        # os.system('rm '+ datafile )
        # input('deleting ctrl-c to cancel, enter to continue')
        # h5file = h5py.File( datafile, 'w')
        None

'''
Locate Data
'''
VHI_FILES = glob.glob('./data/raster/VHI/VHI_*.tif')

SPI03_FILES = glob.glob('./data/raster/SPI/SPI03/spi_03_*.tif')
SPI06_FILES = glob.glob('./data/raster/SPI/SPI06/spi_06_*.tif')
SPI01_FILES = glob.glob('./data/raster/SPI/SPI01/spi_01_*.tif')
SPI12_FILES = glob.glob('./data/raster/SPI/SPI12/spi_12_*.tif')

IIS3_FILES =  glob.glob('./data/raster/IIS3/IIS3_*.tif')
RZSM_FILES =  glob.glob('./data/raster/RZSM/RZSM_*.tif')


'''
Load Shapefiles
'''
brazil = gpd.read_file('./data/shapefile/BR_borders/BR_MUN_WGS84.shp')



def parsefiles(i_kind,FILES):
    '''
    ----------------------------------------
    Indicator Function
    ----------------------------------------
    i_kind :: str - indicator type 
    indicator_files :: list - filelocations
    
    '''
    #group
    try: indicator = h5file[i_kind]
    except KeyError: indicator = h5file.create_group(i_kind)

    nfiles = len(FILES)
    print('Number of %s files'%i_kind, nfiles)

    for counter,f in enumerate(FILES):
        start = time.time()
        '''
        Iterate over each county for each file
        - less IO overhead this way
        '''
        data = rasterio.open(f)
        fname = f.split('/')[-1].replace('.tif','').replace(i_kind+'_','')
        if i_kind == 'VHI' or i_kind == 'IIS3' or i_kind == 'RZSM':
            fname = fname.split('_')
            fname = '%s-%s'%(fname[1],fname[0])
        else:
            fname = '%s-%s'%(fname[0:4],fname[4:])
        


        ###
        ## DRAW
        ###
        if not os.path.exists('%s%s_%s.png'%(imageloc,fname,i_kind)):
            dc.getpng(f,fname,i_kind,imageloc)
        
        
        for shape in brazil.iterrows():
            
            selection = shape[1].geometry
            sname = str(shape[1].GEOCODIGO)
            
            name = shape[1].NOME
            if not name: continue

            '''## subgroup'''
            try: indicator_sub = indicator[sname]
            except KeyError: indicator_sub = indicator.create_group(sname)

            ## clip
            try:clipped_array, clipped_transform = mask(data, [mapping(selection)], crop=True)
            except ValueError: continue

            masked = where(clipped_array<=data.meta['nodata'],nan,clipped_array)

            
            # try: nanmax(masked)
            # except RuntimeWarning: continue
            if not isfinite(masked.any()): continue


            '''## save data'''
            try: dset = indicator_sub[fname]
            except KeyError:
                
                ### create dataset
                dset = indicator_sub.create_dataset(fname, masked.shape, dtype='float32')
                dset[:] = masked
                dset.attrs['transform']= clipped_transform       
                dset.attrs['geocode']=shape[1].GEOCODIGO
                dset.attrs['name']=name
                
                ### dataset
                dset.attrs['max'] = nanmax(masked)
                dset.attrs['min'] = nanmin(masked)
                dset.attrs['median'] = nanmedian(masked)
                dset.attrs['mean'] = nanmean(masked)
                dset.attrs['std'] = nanstd(masked)
                
        print ('(%d/%d) :: '%(counter+1,nfiles),fname, 'took %.2f minutes'%((time.time()-start)/60) )



''' 
Parse FILES
'''
parsefiles('VHI',VHI_FILES)
parsefiles('IIS3',IIS3_FILES)
parsefiles('RZSM',RZSM_FILES)
parsefiles('spi_01',SPI01_FILES)
parsefiles('spi_12',SPI12_FILES)
parsefiles('spi_03',SPI03_FILES)
parsefiles('spi_06',SPI06_FILES)





'''
Close the hdf5 file cleanly
'''
h5file.close()

os.system('rm demo.png')
