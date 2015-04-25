from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import restful
import os
import sys
import logging

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY_CH1ng3me'

api = restful.Api(app)

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

LOG_FILENAME = 'log.out'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s (%(levelname)s):  %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Determines the destination of the build. Only usefull if you're using Frozen-Flask
app.config['FREEZER_DESTINATION'] = os.path.dirname(os.path.abspath(__file__))+'/../build'

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)

import views

api.add_resource(views.Receiver, '/api/receive') 
api.add_resource(views.Seeder, '/api/seed')
