"""server files
.. module:: server
    :platform: Unix
    :synopsis: Flask app server scripts
.. moduleauthor: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This script is a back end web app script
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
import os, glob
from pathlib import Path
'''
Global arguments
'''
# maximum filesize in megabytes
file_mb_max = 100
# encryption key
app_key = 'CSSP'

# list of allowed allowed extensions
extensions = set(['txt', 'pdf', 'image/png', 'image/tiff','image/gtiff'])
#text/html

# cemaccam: Updated apphome to reflect wherever application is living
apphome = str(Path(__file__).resolve().parents[2]) + os.sep  # '/var/www/dev-AgroClimatic-Monitor/'

### if change set in main/config.py too
STORAGE = apphome + 'uolstorage/Data/' #symbolic link in main repo level 1
PROCESSED = apphome + 'processed/'
DATA = STORAGE+'data/'
STAGING = STORAGE+'upload'
db_loc = apphome+'upload.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
FNEW = PROCESSED + 'filelist.json'




h5locs = glob.glob(PROCESSED+'data_*.h5')


# full path destination for our upload files
# upload_dest = os.path.join(os.getcwd(), 'uploads_folder')
