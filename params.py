indicators = ['VHI','spi_01','spi_03','spi_06','spi_12','IIS3','RZSM']

i_match = 'VHI spi IIS3 RZSM'.split()


dkeys = [
    "",
    "Normal",
    "Abnormally Dry",
    "Moderate Drought",
    "Severe Drought",
    "Extreme Drought",
    "Exceptional Drought",
    ""];
dnames = [
    "",
    "Normal",
    "Dry",
    "Moderate",
    "Severe",
    "Extreme",
    "Exceptional",
    ""];


cat_lims = {"VHI":[[40,30,20,12,6],[100,0]],### VHI is backwards
            "spi_01":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi_03":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi_06":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "spi_12":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "SPI":[[-.5,-.8,-1.3,-1.6,-2],[4,-4]],
            "RZSM":[[30,20,11,6,3],[100,0]],
            "IIS3":[[6,5,4,3,2],[7,0]]
            }
            
            
colours = ['#'+i for i in '003049-003049-d62828-f77f00-fcbf49-eae2b7-eae2b7'.split('-')][::-1]


iloc={
'VHI': './data/raster/VHI/VHI_*.tif',
'spi_03': './data/raster/SPI/SPI03/spi_03_*.tif',
'spi_06': './data/raster/SPI/SPI06/spi_06_*.tif',
'spi_01': './data/raster/SPI/SPI01/spi_01_*.tif',
'spi_12': './data/raster/SPI/SPI12/spi_12_*.tif',
'IIS3':  './data/raster/IIS3/IIS3_*.tif',
'RZSM':  './data/raster/RZSM/RZSM_*.tiff'
}