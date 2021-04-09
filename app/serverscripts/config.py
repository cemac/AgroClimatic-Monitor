import os, glob 
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



### if change set in main/config.py too
STORAGE = 'uolstorage/' #symbolic link in main repo level 1
PROCESSED = __file__.replace('app/serverscripts/config.py','processed/')
DATA = __file__.replace('app/serverscripts/config.py',STORAGE+'data/')
STAGING = __file__.replace('app/serverscripts/config.py',STORAGE+'upload/')
db_loc = os.path.join(__file__.replace('app/serverscripts/config.py','app/'), 'upload.db')




h5locs = glob.glob(PROCESSED+'data_*.h5')


# full path destination for our upload files
# upload_dest = os.path.join(os.getcwd(), 'uploads_folder')
