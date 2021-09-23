# The official startup script for AgroCliMon
# Author: D.Ellis, H burns
# Maintainer: CEMAC
# Institution: University of Leeds.



# lets kill any running screen instances:
screen -XS climate quit;
screen -wipe;
pkill -9 screen;


# create a new screen session named "climate" in detached mode, activate the conda env and execute the app file.

cd ~/ && screen -dmS climate sh -c 'cd AgroClimatic-Monitor/ && miniconda3/bin/pipenv shell && cd app &&  gunicorn --bind 0.0.0.0:5000 wsgi:app
 2>&1 | tee ~/
agr_app_logfile.log; exec bash'

screen -ls
