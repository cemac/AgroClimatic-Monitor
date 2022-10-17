"""server files
.. module:: server
    :platform: Unix
    :synopsis: Flask app server scripts
.. moduleauther: Dan Ellis & Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil
   Project. This script is a back end web app script
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
from .secure_db import *

import sys

print(db_loc)


'''
Usage:
python add_user.py name passkey
'''
args = sys.argv
sqlc = Database(db_loc,app_key)
print('Adding: ',args[1].replace(' ','_'), args[2])

sqlc.add_user( args[1].replace(' ','_'), args[2])

print('Done')
