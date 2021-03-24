# CSSP-Brazil


https://cemac.github.io/CSSP-Brazil/static/droughtcompare.html



## Processing

- newdata2h5 : run to generate netcdf
- dataconvert : used by netcdf
- prediction_individual : gets json data for individual
- get5indicators.py : joint plot file



## folders

- data : raster data and shapefiles
- processed : netcdf and individual 
- static : web map plot (copy images 'plotdata' to here)
- serverapp : dynamic file upload





## Bundles
This should only be needed if developing new scripts.


### Global NPM 
```
conda install nodejs
npm install --global webpack
cd app/templates/bundles/
npm install

```
### Compilation (if changes are made)
```
conda activate cssp
cd app/templates/bundles/
python webpack.py 
```