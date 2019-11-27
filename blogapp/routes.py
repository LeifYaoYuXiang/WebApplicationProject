# encoding:utf-8
# 此处我们定义了一系列的路由

# 首先是从已有的模块中实现需要模块的引入

#
from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
#
from blogapp import app,db
#
from blogapp.config import Config
from blogapp.form import LoginFrom, SignUpForm
from blogapp.models import User
#
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    # 这里我们先将引入的LoginForm表单传给一个变量，之后的操作将基于对表单form的监听加以实现
    form = LoginFrom()
    # 对提交按钮的监听
    if form.validate_on_submit():
        # 在User的表中查找匹配的username
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('')
            return redirect(url_for(login))
        if(check_password_hash(user_in_db.password_hash,form.password.data)):
            flash('')
            session['USERNAME']=user_in_db.username
            session['USER_ID']=user_in_db.id
            return redirect(url_for(index))
        flash('Incorrect Password')
    # 在这里我们渲染所需要的页面并且及时返回给前端，我们在渲染的时候将form传入进去作为参数
    return render_template('login.html',form=form)


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user_in_db=User.query.filter(User.username == form.username.data).first()
        if user_in_db:
            flash('Identical User Name, Please use another one')
        if form.password.data != form.password_ensure.data:
            flash('Password don\'t match')
        password_hash=generate_password_hash(form.password.data)

    return render_template('sign_up.html',form=form)


@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template('contact.html')


@app.route('/album',methods=["GET","POST"])
def album():
    return render_template('album.html')


@app.route('/resources',methods=["GET","POST"])
def resources():
    return render_template('resources.html')


# @app.route('/contact',methods=["GET","POST"])
# def contact():
#     return render_template('contact.html')