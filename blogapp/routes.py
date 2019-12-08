# encoding:utf-8
# 此处我们定义了一系列的路由

from flask import render_template, flash, redirect, url_for, session, send_from_directory, request
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app,db
from blogapp.config import Config
from blogapp.form import LoginFrom, SignUpForm,CommentForm
from blogapp.models import User, Blog, Comment, Resource
import os


@app.route('/')
@app.route('/index')
def index():
    username = session.get("USERNAME")
    path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'templates'+os.sep+'blogs'
    files = os.listdir(path)
    all_blog_information = []
    for file in files:
        name = os.path.splitext(file)[0]
        print(name)
        blog = Blog.query.filter_by(title=name).first()
        if blog:
            print(blog.id)
            comments = Comment.query.filter_by(blog_id=blog.id).count()
            all_blog_information.append({'title': name,'tag': blog.tag,'click': blog.click, 'time': blog.time,'comment': comments})
    return render_template('index.html', all_blog_information=all_blog_information, username=username)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('No User Found')
            return redirect(url_for('login'))
        if(check_password_hash(user_in_db.password_hash, form.password.data)):
            flash('Login Success')
            session['USERNAME']=user_in_db.username
            session['USER_ID']=user_in_db.id
            return redirect(url_for("index"))
        flash('Incorrect Password')
    return render_template('login.html', form=form)


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password_hash=password_hash, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        session["USERNAME"] = user.username
        session['USERID'] = user.id
        return redirect(url_for('login'))
    return render_template('sign_up.html', form=form)


@app.route('/contact',methods=["GET", "POST"])
def contact():
    return render_template('contact.html')


@app.route('/album',methods=["GET", "POST"])
def album():
    return render_template('album.html')


@app.route('/resources',methods=["GET", "POST"])
def resources():
    path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'static' + os.sep + 'download'
    files = os.listdir(path)
    resources_in_db = []
    for file in files:
        name = os.path.splitext(file)[0]
        resource = Resource.query.filter_by(name=name).first()
        if resource:
            f_pos = os.path.getsize(path+os.sep+file)
            fsize = round(f_pos / float(1024), 2)
            type = os.path.splitext(file)[1]
            if type=='.zip':
                type = 'ZIP'
            elif type == '.apk':
                type = 'APK'
            elif type == '.ppt':
                type = 'PPT'
            elif type == '.py':
                type = 'PYTHON'
            elif type == '.pdf':
                type = 'PDF'
            elif type == '.xls':
                type = 'EXCEL'
            elif type == '.doc':
                type = 'DOC'
            resources_in_db.append({'name': resource.name,'description': resource.description,'tag':resource.tag, 'download':resource.download, 'size':fsize, 'type':type})
        else:
            print("NOT FOUND")
    print(resources_in_db)
    return render_template('resources.html',resources_in_db=resources_in_db)


@app.route('/resources_search/<keyword>',methods=["GET", "POST"])
def resources_search(keyword):
    path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'static' + os.sep + 'download'
    files = os.listdir(path)
    resources_in_db = []
    if keyword in ['JAVA','C','OPENGL','FLASK','ANDROID','PYTHON']:
        for file in files:
            name = os.path.splitext(file)[0]
            resource = Resource.query.filter_by(name=name, tag=keyword).first()
            if resource:
                f_pos = os.path.getsize(path + os.sep + file)
                fsize = round(f_pos / float(1024), 2)
                type = os.path.splitext(file)[1]
                if type == '.zip':
                    type = 'ZIP'
                elif type == '.apk':
                    type = 'APK'
                elif type == '.ppt':
                    type = 'PPT'
                elif type == '.py':
                    type = 'PYTHON'
                elif type == '.pdf':
                    type = 'PDF'
                elif type == '.xls':
                    type = 'EXCEL'
                elif type == '.doc':
                    type = 'DOC'
                resources_in_db.append({'name': resource.name, 'description': resource.description, 'tag': resource.tag,
                                        'download': resource.download, 'size': fsize, 'type': type})
            else:
                print("NOT FOUND")
        print(resources_in_db)
    else:
        print('HELLO')
        for file in files:
            type = os.path.splitext(file)[1]
            if type == '.zip':
                type = 'ZIP'
            elif type == '.apk':
                type = 'APK'
            elif type == '.ppt':
                type = 'PPT'
            elif type == '.py':
                type = 'PYTHON'
            elif type == '.pdf':
                type = 'PDF'
            elif type == '.xls':
                type = 'EXCEL'
            elif type == '.doc':
                type = 'DOC'
            name = os.path.splitext(file)[0]
            resource = Resource.query.filter_by(name=name).first()
            if resource and type==keyword:
                f_pos = os.path.getsize(path + os.sep + file)
                fsize = round(f_pos / float(1024), 2)
                resources_in_db.append({'name': resource.name, 'description': resource.description, 'tag': resource.tag,
                                        'download': resource.download, 'size': fsize, 'type': type})
    return render_template('resources_search.html', keyword=keyword,resources_in_db=resources_in_db)


@app.route('/game',methods=['GET','POST'])
def game():
    return render_template('game.html')


@app.route('/pictureDisplay/<type>', methods=['GET','POST'])
def pictureDisplay(type):
    print(type)
    path = '';
    temp_pics = [];
    pics = [];
    if type == "ACG":
        path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'static'+os.sep+'assets'+os.sep+'album_acg'
        temp_pics = os.listdir(path)
        for pic in temp_pics:
            pic = 'assets/album_acg/'+pic
            print(pic)
            pics.append(pic)
        print(pics)
    elif type == "LIFE":
        path = os.path.split(os.path.realpath(__file__))[0] +os.sep+'static'+os.sep+'assets'+os.sep+'album_life'
        temp_pics = os.listdir(path)
        for pic in temp_pics:
            pic = 'assets/album_life/' + pic
            print(pic)
            pics.append(pic)
        print(pics)
    elif type == "PAINTING":
        path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'static'+os.sep+'assets'+os.sep+'album_painting'
        temp_pics = os.listdir(path)
        for pic in temp_pics:
            pic = 'assets/album_painting/' + pic
            print(pic)
            pics.append(pic)
        print(pics)
    elif type == "MOVIE":
        path = os.path.split(os.path.realpath(__file__))[0] +os.sep+'static'+os.sep+'assets'+os.sep+'album_movie'
        temp_pics = os.listdir(path)
        for pic in temp_pics:
            pic = 'assets/album_movie/' + pic
            print(pic)
            pics.append(pic)
        print(pics)
    elif type == 'PLACES':
        path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'static'+os.sep+'assets'+os.sep+'album_places'
        temp_pics = os.listdir(path)
        for pic in temp_pics:
            pic = 'assets/album_places/' + pic
            print(pic)
            pics.append(pic)
        print(pics)
    elif type == "WALLPAPER":
        path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'static'+os.sep+'assets'+os.sep+'album_wallpaper'
        temp_pics = os.listdir(path)
        for pic in temp_pics:
            pic = 'assets/album_wallpaper/' + pic
            print(pic)
            pics.append(pic)
        print(pics)
    return render_template('pictureDisplay.html',pics=pics)


@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        path = os.path.split(os.path.realpath(__file__))[0] + os.sep+'static'+os.sep+'download'+os.sep+filename
        if os.path.isfile(path):
            dir = os.path.split(os.path.realpath(__file__))[0] + os.sep+'static'+os.sep+'download'
            return send_from_directory(dir, filename, as_attachment=True)
        pass


@app.route('/blogContent/<string:blog_name>',methods=['GET','POST'])
def blogContent(blog_name):
    blog = Blog.query.filter_by(title=blog_name).first()
    blog.click = blog.click+1

    db.session.add(blog)
    db.session.commit()

    form = CommentForm()
    blog_name = 'blogs/'+blog_name+'.html'
    print(blog_name)
    print(blog.id)
    comments=[]
    comments_in_db = Comment.query.filter(Comment.blog_id == blog.id).all();
    for comment in comments_in_db:
        username = User.query.filter(User.id == comment.user_id).first()
        comments.append({'username': username, 'information': comment.information})

    username = session.get("USERNAME")
    if username:
        print("HAVE LOG IN")
        if form.validate_on_submit():
            print(session.get('USERNAME'))
            user_in_db = User.query.filter(User.username == session.get('USERNAME')).first()
            comment = Comment(information=form.comment.data,blog_id=blog.id,user_id=user_in_db.id)
            db.session.add(comment)
            db.session.commit()
    else:
        print("HAVE NOT LOG IN")
    return render_template('blogContent.html', name=blog_name, form=form,comments_in_db=comments)