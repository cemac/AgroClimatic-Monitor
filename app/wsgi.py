# WSGI script for mod_wgsi to use
# Step one activate python environment via bespoke activate_this.py (supplied in repo)
activate_this = '/var/www/agro-python/bin/activate_this.py'

with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))
# Tell mod_wsgi the root dir of the app        
import sys
sys.path.insert(0, '/var/www/AgroClimatic-Monitor/')

# The standard wgsi import
from app import app as application
