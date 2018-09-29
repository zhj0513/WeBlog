from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('真名：', validators=[Length(0, 64)])
    location = StringField('地址：', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我：')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱：', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名：', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^([\u4e00-\u9fa5]|[A-Za-z0-9_.]){1,8}$', 0,
               '用户名过长')])
    confirmed = BooleanField('已验证')
    role = SelectField('权限：', coerce=int)
    name = StringField('真名：', validators=[Length(0, 64)])
    location = StringField('地址：', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我：')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class PostForm(FlaskForm):
    body = PageDownField("随便写点什么  ╮(￣▽￣)╭", validators=[DataRequired()])
    submit = SubmitField('发表')


class CommentForm(FlaskForm):
    body = StringField('评论一下', validators=[DataRequired()])
    submit = SubmitField('发表')

