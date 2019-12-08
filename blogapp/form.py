# encoding:utf-8
# 在form.py中，我们定义了一系列即将用于web网页的表单，我们在此定义表单中包含的元素，以及对元素的相关检验

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
    username = StringField('Input Username', validators=[DataRequired()])
    password = PasswordField('Input Password', validators=[DataRequired()])
    password_ensure = PasswordField('Input your password again',validators=[DataRequired()])
    email = StringField('Input Your Email',validators=[DataRequired(),email()])
    accept_rules = BooleanField('I accept the site rules',validators=[DataRequired()])
    submit = SubmitField('Register')


class CommentForm(FlaskForm):
    comment = TextAreaField("Please made your comments",validators=[DataRequired()])
    submit = SubmitField('Comment')