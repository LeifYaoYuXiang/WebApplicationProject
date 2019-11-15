#encoding:utf-8
from blogapp import app
from flask import render_template
from blogapp.form import LoginFrom


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginFrom()
    return render_template('login.html',form=form)