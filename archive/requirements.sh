#!/bin/bash


conda create -n cssp python=3.8 && source activate cssp


git clone https://github.com/scikit-learn/scikit-learn.git
cd scikit-learn
pip install cython pmdarima seaborn
make 
pip uninstall scikit-learn
python setup.py install


pip install pip pandas geopandas descartes rasterio h5py topojson flask sktime
pip install topojson
pip install jupyterlab notebook

pip install sktime[all_extras]

python -m pip install https://github.com/alan-turing-institute/sktime/archive/v0.5.2.tar.gz



sudo pip install pandas geopandas descartes rasterio h5py topojson

h5py flask sktime
