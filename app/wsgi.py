"""WSGI scrip
.. module:: wsgi
    :platform: Unix
    :synopsis:  WSGI script for mod_wgsi to use
.. moduleauther: Helen Burns @ CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the CSSP Brazil 
   Project. This Script passes information about the python environment to the
   web server
   :copyright: © 2022 University of Leeds.
   :license: GPL-3.0
Example:
    To use::
        python app.py
        It is best to run this app via a web server gunicorn or Apache
.. AgroClimatic-Monitor:
   https://github.com/cemac/AgroClimatic-Monitor
"""
# WSGI script for mod_wgsi to use
# Step one activate python environment via bespoke activate_this.py (supplied in repo)
#activate_this = '/var/www/agro-python/bin/activate_this.py'
#
#with open(activate_this) as file_:
#       exec(file_.read(), dict(__file__=activate_this))
#python_home='/var/www/miniconda3/envs/agro-python/'
python_home='/var/www/agro-python/'
import sys
import site
# Calculate path to site-packages directory.
python_version = '.'.join(map(str, sys.version_info[:2]))
site_packages = python_home + '/lib/python%s/site-packages' % python_version
# Remember original sys.path.

prev_sys_path = list(sys.path)
# Add the site-packages directory.
site.addsitedir(site_packages)

# Reorder sys.path so new directories at the front.

new_sys_path = []

for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)

sys.path[:0] = new_sys_path

# Tell mod_wsgi the root dir of the app
sys.path.insert(0, '/var/www/AgroClimatic-Monitor/')
sys.path.insert(0, '/var/www/AgroClimatic-Monitor/app/')
import os
os.environ["TMPDIR"] = "/var/www/tmp/"
os.environ["TMP"] = "/var/www/tmp/"
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("PATH:", os.environ.get('PATH'))
# The standard wgsi import
from app import app as application
