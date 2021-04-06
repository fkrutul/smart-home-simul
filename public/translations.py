#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
import jinja2
app = Flask(__name__)
app.config["BABEL DEFAULT_LOCALE"] = 'en'
babel = Babel(app)
jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
@babel.localeselector
def get_locale():
    return 'fr'
    return request.accept.languages.best_match(['en', 'fr'])

@app.route('/')
def index():
    lights = gettext('Lights')
    masterBedroom = gettext('Master Bedroom')
    bedroom = gettext('Bedroom')
    kitchen = gettext('Kitchen')
    bathroom = gettext('Bathroom')
    garage = gettext('Garage')
    livingRoom = gettext('Living Room')

    return render_template('index.html', lights=lights, masterBedroom=masterBedroom, bedroom=bedroom, kitchen=kitchen,
    bathroom=bathroom, garage=garage, livingRoom=livingRoom)      

if __name__ == '__main__':
    app.run(debug=True)
