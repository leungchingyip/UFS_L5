#!/usr/bin/python

activate_this = '/catalog/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0,"/catalog/catalog")
from catalog import app
from werkzeug.debug import DebuggedApplication 
application = DebuggedApplication(app, True)
application.secret_key = 'uuuuuuuuuuuuuuu'
