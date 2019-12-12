# encoding:utf-8
# 在form.py中，我们定义了一系列即将用于web网页的表单，我们在此定义表单中包含的元素，以及对元素的相关检验
# the following code is referenced from Week 10
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,email


# 该表单用于登陆界面
class LoginFrom(FlaskForm):
    # 以下定义了一系列的表单元素
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# 该表单用于申请账户界面
class SignUpForm(FlaskForm):
    # 以下定义了一系列的表单元素
    username = StringField('Input your username', validators=[DataRequired()])
    password = PasswordField('Input your password', validators=[DataRequired()])
    password_ensure = PasswordField('Input your password again',validators=[DataRequired()])
    email = StringField('Input your Email',validators=[DataRequired(),email()])
    accept_rules = BooleanField('I accept the site rules',validators=[DataRequired()])
    submit = SubmitField('Register')


class CommentForm(FlaskForm):
    comment = TextAreaField("",validators=[DataRequired()])
    submit = SubmitField('Comment')


class SearchBlog(FlaskForm):
    search = StringField('search blogs here',validators=[DataRequired()])
    submitSearch = SubmitField('Search')


class SuggestionPost(FlaskForm):
    post = TextAreaField("",validators=[DataRequired()])
    submitSuggestion=SubmitField('Send')