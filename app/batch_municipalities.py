"""CSSP Brazil
.. module:: 
    :platform: Unix
    :synopsis: Batch Script for processing muncipalities
.. moduleauther: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This Script is the main flask application file.
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
Example:
    To use::
        python app.py
        It is best to run this app via a web server gunicorn or Apache
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
from serverscripts.config import *
import pandas as pd
from serverscripts.get_individual_batch import m_new

# this must be run in pip production env
print('DO NOT RUN IN CONDA ENV')
codelist = pd.read_csv(PROCESSED+'geojson/search.csv')
for key in codelist.iterrows():
    code = str(key[1].val)
    try:
        m_new(code)
    except:
        continue
