from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱：', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('自动登录')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱：', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名：', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^([\u4e00-\u9fa5]|[A-Za-z0-9_.]){1,8}$', 0,
               '用户名过长')])
    password = PasswordField('密码：', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册！')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码：', validators=[DataRequired()])
    password = PasswordField('新密码：', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('确认新密码：',
                              validators=[DataRequired()])
    submit = SubmitField('更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱：', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重置密码')


class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码：', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('重置密码')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱：', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('密码：', validators=[DataRequired()])
    submit = SubmitField('更新邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册！')
