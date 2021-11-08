activate_this = '/var/www/agro-python/bin/activate_this.py'

with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))
import sys
sys.path.insert(0, '/var/www/AgroClimatic-Monitor/')

from app import app
if __name__ == "__main__":
    app.run(debug=True)
