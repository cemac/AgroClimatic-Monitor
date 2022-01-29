#!/bin/bash -
#title          :installpreproc.sh
#description    :Install delicate preprocessing environment
#author         :CEMAC - Helen
#date           :2022 Jan
#version        :1
#usage          :./installpreproc.sh
#notes          :
#bash_version   :4.2.46(2)-release
#============================================================================
############################################################################
# Install environment for preprocessing                                    #
#                                                                          #
############################################################################
# Python 3.9 req
echo 'downloading anaconda'
wget
chmod 755
bash
conda activate
echo 'check conda environment activated'
conda create -n agro-python python=3.9
conda activate agro-python
# mamba is quicker and needed to install the correct nodejs
conda install -c conda-forge mamba -y
mamba install nodejs  -y
mamba install -c conda-forge  rioxarray  -y
mamba install -c conda-forge ffmpeg  -y
mamba install -c conda-forge imagemagick  -y
mamba install -c conda-forge geopandas  -y
mamba install -c conda-forge h5py -y
mamba install -c conda-forge  rasterio -y
mamba install pip  -y
pip install Markdown
pip install simplejson
pip install Flask
pip install Flask-SocketIO
pip install Flask-SQLAlchemy
pip install flask-statistics
# YOU MUST deactivate and activate to set environment variables
conda deactivate agro-python
conda activate agro-python

# Notes
# Nodejs must be >7
# python must be >3.7
# working version is frozen in yml file
# environment is fragile any breakage it is best to restart from scratch
# python must be python 3.6 backwards compatible to work on leeds server pip environment
