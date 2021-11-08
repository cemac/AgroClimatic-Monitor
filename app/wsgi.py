activator = '/var/www/agro-python/bin//activate_this.py'  
with open(activator) as f:
    exec(f.read(), {'__file__': activator})
import sys
sys.path.insert(0, '/var/www/AgroClimatic-Monitor/app')
from app import app
if __name__ == "__main__":
    app.run(debug=True)
