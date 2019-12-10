# encoding:utf-8
# 此处我们定义了一系列的路由

from flask import render_template, flash, redirect, url_for, session, send_from_directory, request
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp import app,db
from blogapp.config import Config
from blogapp.form import LoginFrom, SignUpForm,CommentForm,SearchBlog,SuggestionPost
from blogapp.models import User, Blog, Comment, Resource,Suggesstion
import os
import random


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchBlog()
    username = session.get("USERNAME")
    path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'templates'+os.sep+'blogs'
    files = os.listdir(path)
    all_blog_information = []
    original = Blog.query.filter_by().count()
    fans = User.query.filter_by().count()
    comments_total=Comment.query.filter_by().count()

    java_blog = Blog.query.filter_by(tag='Java').count()
    c_blog = Blog.query.filter_by(tag='C').count()
    flask_blog = Blog.query.filter_by(tag='Flask').count()
    opengl_blog = Blog.query.filter_by(tag='OpenGL').count()
    android_blog = Blog.query.filter_by(tag='Android').count()
    python_blog = Blog.query.filter_by(tag='Python').count()
    for file in files:
        name = os.path.splitext(file)[0]
        blog =Blog.query.filter_by(title=name).first()
        if blog:
            comments = Comment.query.filter_by(blog_id=blog.id).count()
            all_blog_information.append({'title': name,
                                         'tag': blog.tag,
                                         'click': blog.click,
                                         'time': blog.time,
                                         'comment': comments})
    all_blog_information.sort(key=lambda x: x["click"],reverse=True)
    if form.validate_on_submit():
        keyword=form.search.data
        return redirect(url_for('blog_search',keyword=keyword))
    return render_template('index.html', all_blog_information=all_blog_information,
                           username=username,
                           form=form,
                           original=original,
                           fans=fans,
                           comments_total=comments_total,
                           java_blog=java_blog,
                           c_blog=c_blog,
                           flask_blog=flask_blog,
                           opengl_blog=opengl_blog,
                           android_blog=android_blog,
                           python_blog=python_blog)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginFrom()
    username=session.get('USERNAME')
    if username:
        flash('You have log in one account,may you want to log in another one')
    else:
        flash('You have not log in! Please log in and then you are able to make comments')
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
    return render_template('login.html', form=form,username=username)


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
    form=SuggestionPost()
    log_in_username = session.get("USERNAME")
    if log_in_username:
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.username == session.get('USERNAME')).first()
            suggestion = Suggesstion(suggestion=form.post.data,user_id=user_in_db.id)
            db.session.add(suggestion)
            db.session.commit()
            form.post.data = ""
            last_post={'information':suggestion.suggestion}
            return render_template('contact.html',form=form,last_post=last_post)
    else:
        flash("You have not log in yet!")
    return render_template('contact.html',form=form,username=log_in_username)


@app.route('/album', methods=["GET", "POST"])
def album():
    log_in_username = session.get("USERNAME")
    return render_template('album.html',username=log_in_username)


@app.route('/resources',methods=["GET", "POST"])
def resources():
    log_in_username = session.get("USERNAME")
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
            elif type == '.jar':
                type = 'JAR'
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
    return render_template('resources.html',resources_in_db=resources_in_db,username=log_in_username)


@app.route('/resources_search/<keyword>',methods=["GET", "POST"])
def resources_search(keyword):
    log_in_username = session.get("USERNAME")
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
                elif type == '.jar':
                    type = 'JAR'
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
        for file in files:
            type = os.path.splitext(file)[1]
            if type == '.zip':
                type = 'ZIP'
            elif type == '.jar':
                type = 'JAR'
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
    return render_template('resources_search.html', keyword=keyword,resources_in_db=resources_in_db,username=log_in_username)


@app.route('/game',methods=['GET','POST'])
def game():
    return render_template('game.html')


@app.route('/pictureDisplay/<type>', methods=['GET','POST'])
def pictureDisplay(type):
    username=session.get('USERNAME')
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
    return render_template('pictureDisplay.html',pics=pics,username=username)


@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        path = os.path.split(os.path.realpath(__file__))[0] + os.sep+'static'+os.sep+'download'+os.sep+filename
        print(path)
        if os.path.isfile(path):
            dir = os.path.split(os.path.realpath(__file__))[0] + os.sep+'static'+os.sep+'download'
            item_name=os.path.splitext(filename)[0]
            print(item_name)
            resource_download = Resource.query.filter_by(name=item_name).first()
            resource_download.download=resource_download.download+1
            db.session.add(resource_download)
            db.session.commit()
            return send_from_directory(dir, filename, as_attachment=True)
        pass


@app.route('/blogContent/<string:blog_name>',methods=['GET','POST'])
def blogContent(blog_name):
    blog = Blog.query.filter_by(title=blog_name).first()
    blog.click = blog.click+1

    db.session.add(blog)
    db.session.commit()

    original = Blog.query.filter_by().count()
    fans = User.query.filter_by().count()
    comments_total = Comment.query.filter_by().count()
    java_blog = Blog.query.filter_by(tag='Java').count()
    c_blog = Blog.query.filter_by(tag='C').count()
    flask_blog = Blog.query.filter_by(tag='Flask').count()
    opengl_blog = Blog.query.filter_by(tag='OpenGL').count()
    android_blog = Blog.query.filter_by(tag='Android').count()
    python_blog = Blog.query.filter_by(tag='Python').count()

    form = CommentForm()
    blog_path = 'blogs/'+blog_name+'.html'

    comments=[]
    comments_in_db = Comment.query.filter(Comment.blog_id == blog.id).all()
    for comment in comments_in_db:
        icon_index = str(random.randint(1, 6))
        username = User.query.filter(User.id == comment.user_id).first()
        comments.append({'username': username.username, 'information': comment.information,'icon':icon_index})

    log_in_username = session.get("USERNAME")
    if log_in_username:
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.username == session.get('USERNAME')).first()
            comment = Comment(information=form.comment.data,blog_id=blog.id,user_id=user_in_db.id)
            db.session.add(comment)
            db.session.commit()
            form.comment.data=""
            return redirect(url_for('blogContent', blog_name=blog_name))
    else:
        flash("You have not log in yet!")
    return render_template('blogContent.html',
                           name=blog_path,
                           form=form,
                           comments_in_db=comments,
                           original=original,
                           fans=fans,
                           comments_total=comments_total,
                           java_blog=java_blog,
                           c_blog=c_blog,
                           flask_blog=flask_blog,
                           opengl_blog=opengl_blog,
                           android_blog=android_blog,
                           python_blog=python_blog,
                           username=log_in_username)


@app.route('/blog_search/<keyword>',methods=['GET','POST'])
def blog_search(keyword):
    username = session.get("USERNAME")
    path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'templates' + os.sep + 'blogs'
    files = os.listdir(path)
    search_blog_information = []
    for file in files:
        name = os.path.splitext(file)[0]
        blog =Blog.query.filter(Blog.title == name, or_(Blog.title.like('%'+keyword+'%'), Blog.tag.like('%'+keyword+'%'))).first()
        if blog:
            print(blog.id)
            comments = Comment.query.filter(Comment.blog_id==blog.id).count()
            search_blog_information.append({'title': name,'tag': blog.tag,'click': blog.click, 'time': blog.time,'comment': comments})
    original = Blog.query.filter_by().count()
    fans = User.query.filter_by().count()
    comments_total = Comment.query.filter_by().count()

    java_blog = Blog.query.filter_by(tag='Java').count()
    c_blog = Blog.query.filter_by(tag='C').count()
    flask_blog = Blog.query.filter_by(tag='Flask').count()
    opengl_blog = Blog.query.filter_by(tag='OpenGL').count()
    android_blog = Blog.query.filter_by(tag='Android').count()
    python_blog = Blog.query.filter_by(tag='Python').count()

    return render_template('blog_search.html',
                           search_blog_information=search_blog_information,
                           keyword=keyword,
                           username=username,
                           original=original,
                           fans=fans,
                           comments_total=comments_total,
                           java_blog=java_blog,
                           c_blog=c_blog,
                           flask_blog=flask_blog,
                           opengl_blog=opengl_blog,
                           android_blog=android_blog,
                           python_blog=python_blog)