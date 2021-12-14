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

apphome = '/var/www/AgroClimatic-Monitor/'

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
