'''
Process individual hdf5 FILES

CSSP brazil
written by d.ellis@leeds.ac.uk for CEMAC
'''

import geopandas as gpd
import rasterio,h5py,glob,time
from rasterio import MemoryFile
from rasterio.mask import mask,raster_geometry_mask
from shapely.geometry import mapping

from numpy import ma,nan,where,nanmean,nanstd,nanmedian,nanmax,nanmin,isfinite
from matplotlib import pyplot as plt
import matplotlib as mpl
import os,warnings,sys
import dataconvert as dc
import config as cf

from params import cat_lims,colours
warnings.filterwarnings('ignore', category=RuntimeWarning)

'''
Load Shapefiles
'''
brazil = gpd.read_file(cf.DATA+'shapefile/BR_borders/BR_MUN_WGS84.shp')
breakearly = False



def parsefiles(i_kind,FILES,dataloc,imageloc):
    '''
    ----------------------------------------
    Indicator Function
    ----------------------------------------
    i_kind :: str - indicator type
    indicator_files :: list - filelocations
    dataloc :: str - data Location
    imageloc :: str - image location for saving
    '''
    print(i_kind,FILES,dataloc,imageloc)
    print(i_kind, imageloc,dataloc)

    thisfile = '%sdata_%s.h5'%(dataloc,i_kind)
    if os.path.exists(thisfile):
        basetime = os.path.getmtime(thisfile)
    else:
        basetime=-0

    try:
        indicator = h5py.File( thisfile , 'a')

    except:
            # try closing all instances of the file first
            basetime = -1
            os.system('rm '+ thisfile )
            # input('deleting ctrl-c to cancel, enter to continue')
            # h5file = h5py.File( datafile, 'w')
            print('FAILED retrying')
            indicator = h5py.File( thisfile , 'a')
            None



    FILES = glob.glob(FILES)
    nfiles = len(FILES)
    print('Number of %s files'%i_kind, nfiles)



    '''
    CBAR
    '''
    cat = cat_lims[i_kind]

    # bins = [cat_lims[1][0]]
    # bins.extend(cat_lims[0])


    bins = [cat[1][0]]
    bins.extend(cat[0])
    bins.append(cat[1][1])

    col = colours

    if bins[-1]<bins[0]:
        print('REVERSEcolour', i_kind)
        bins = bins[::-1]
        cols = colours[::-1]

    # assert len(bins)-1 == len(colours)
    cmap = mpl.colors.ListedColormap(col)
    norm = mpl.colors.BoundaryNorm(boundaries=bins, ncolors=len(cmap.colors)-1 )

    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)
    cb2 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                    norm=norm,
                                    boundaries=  bins ,
                                    extend='both',
                                    ticks=bins,
                                    spacing='proportional',
                                    orientation='horizontal')
    cb2.set_label(i_kind)
    plt.savefig(imageloc+i_kind+'.png',  transparent=True,bbox_inches='tight',pad_inches=0)












    for counter,f in enumerate(FILES):
        start = time.time()
        '''
        Iterate over each county for each file
        - less IO overhead this way
        '''

        if basetime>os.path.getmtime(f):
            print('Skipping:',f ,basetime, os.path.getmtime(f) )
            continue # this file is older than the combigned one - ignore.

        data = rasterio.open(f)
        fname = f.split('/')[-1].replace('.tiff','').replace('.tif','').replace(i_kind+'_','')
        print(fname)
        if i_kind == 'VHI' or i_kind == 'IIS3':
            fname = fname.split('_')
            fname = '%s-%s'%(fname[1],fname[0])
        elif i_kind == 'RZSM':
            fname = fname.split('_')
            fname = '%s-%s'%(fname[0],fname[1])
        else:
            fname = '%s-%s'%(fname[0:4],fname[4:])



        ###
        ## DRAW
        ###
        if not os.path.exists('%s%s_%s.png'%(imageloc,fname,i_kind)):
            dc.getpng(f,fname,i_kind,cmap,norm,imageloc)


        for shape in brazil.iterrows():

            selection = shape[1].geometry
            sname = str(shape[1].GEOCODIGO)
            print(sname)
            name = shape[1].NOME
            if not name: continue

            '''## subgroup'''
            try: indicator_sub = indicator[sname]
            except KeyError: indicator_sub = indicator.create_group(sname)

            ## clip
            try:clipped_array, clipped_transform = mask(data, [mapping(selection)], crop=True)
            except ValueError: continue


            # MASK based on max limit
            if i_kind != 'IIS3':
                masked = where(clipped_array<=data.meta['nodata'],nan,clipped_array)
            else:
                masked = where(clipped_array>=data.meta['nodata'],nan,clipped_array)


            # try: nanmax(masked)
            # except RuntimeWarning: continue
            if not isfinite(masked.any()): continue


            '''## save data'''
            try:
                dset = indicator_sub[fname]
                if breakearly:
                    break # skip all muncipalities as we have the data for this timestep file.
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
                #
                # print('----',dset.attrs['min'],dset.attrs['max'])
        print ('(%d/%d) :: '%(counter+1,nfiles),fname, 'took %.2f minutes'%((time.time()-start)/60) )

    '''
    Close the hdf5 file cleanly
    '''
    indicator.close()
    return i_kind+' finished'

if __name__ == '__main__':
#     print(sys.argv)
    parsefiles(*sys.argv[1:5])
