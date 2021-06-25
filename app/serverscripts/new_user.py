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