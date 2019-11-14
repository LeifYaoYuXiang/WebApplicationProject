from flask import Flask,render_template
from blogapp.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from blogapp import routes