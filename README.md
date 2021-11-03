# CSSP-Brazil

<img data-toggle="modal" data-target="[data-modal='10.5281-zenodo.4644359']" src="https://zenodo.org/badge/301839203.svg" alt="10.5281/zenodo.4644359">



# Viewing the machine (pre global or VPN release)
1. Navigate to https://vwd.leeds.ac.uk/ and log into the virtual desktop
2. open chrome
3. navigate to http://129.11.78.152:57263
4. 

# Developer Guide

Information for developers is found in our [wiki](https://github.com/cemac/AgroClimatic-Monitor/wiki/Developer-Guide)

<hr>

# QuickStart - Running the app locally

1. clone this repository
2. check and install the requirements
3. to run the app
`cd app/ && python wsgi.py`
**or**
`cd app/ && gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile=~/logs/app/access.log
--error-logfile=~/logs/app/error.log --access-logformat='%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' wsgi:app `

# Requirements

## pip

Recomended pip install using system python to create virtual environment

```bash
python -m venv agro-python
source agro-python/bin/activate
pip install -r requirements.txt
```

## conda

```
https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

#### update base to include data
```
conda install pip;
conda env update --file local.yml

```

<hr>

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
