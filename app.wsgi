#app.wsgi
import sys
sys.path.insert(0, '/var/www/html/newsanalyzer')

from app import app as application