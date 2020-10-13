import geopandas as gpd  
import rasterio,h5py,glob,time
from rasterio import MemoryFile
from rasterio.mask import mask,raster_geometry_mask
from shapely.geometry import mapping

from numpy import ma,nan,where,nanmean,nanstd,nanmedian,nanmax,nanmin

'''
Open HDF5 datafile
'''
h5file = h5py.File('processed/data.h5', 'a')


'''
Locate Data
'''
VHI_FILES = glob.glob('./data/raster/VHI/VHI_*.tif')
SPI03_FILES = glob.glob('./data/raster/SPI/SPI03/spi_03_*.tif')
SPI06_FILES = glob.glob('./data/raster/SPI/SPI06/spi_06_*.tif')


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

        for shape in brazil.iterrows():
            
            selection = shape[1].geometry
            sname = shape[1].NOME
            
            if not sname: continue

            ## subgroup
            try: indicator_sub = indicator[fname]
            except KeyError: indicator_sub = indicator.create_group(fname)

            ## clip
            try:clipped_array, clipped_transform = mask(data, [mapping(selection)], crop=True)
            except ValueError: continue

            masked = where(clipped_array<=data.meta['nodata'],nan,clipped_array)

            ## save data
            try: dset = indicator_sub[sname]
            except KeyError:
                
                ### create dataset
                dset = indicator_sub.create_dataset(sname, masked.shape, dtype='float32')
                dset[:] = masked
                dset.attrs['transform']= clipped_transform       
                dset.attrs['geocode']=shape[1].GEOCODIGO
                
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
parsefiles('spi_03',SPI03_FILES)
parsefiles('spi_06',SPI06_FILES)





'''
Close the hdf5 file cleanly
'''
h5file.close()

