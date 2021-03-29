# CSSP-Brazil

https://cemac.github.io/CSSP-Brazil/app/

# VM 

1. Login to the see gateway
2. ssh 129.11.78.152


## install conda 
```
https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

### update base to include data
``` 
conda install pip;
conda env update --file local.yml 

```

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


## Shapefile 



## User Credentials 
These are contained within an encrypted sqlite database. (Note that the code for this only seems to work on linux machines like the VM).


### Adding a new user 
From the main directory
```
python -m app.serverscripts.new_user UserName SecretCodeToEnter
```
If a password has already been used you will get an error containing 
`UNIQUE constraint failed`


### When initiating we need to build the database.
```
python -m app.serverscripts.secure_db --wipe
```


# template_br
These are identical to the normal template, except that they have 
