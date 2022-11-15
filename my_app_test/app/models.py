import pymysql
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import db, login
from datetime import datetime
from sqlalchemy.sql.sqltypes import LargeBinary
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# db.metadata.clear()

class FileVersion(db.Model):
    __tablename__ = 'file_version'
    file_id = Column(Integer, ForeignKey('file.id'), primary_key=True)
    version_id = Column(Integer, ForeignKey('version.id'), primary_key=True)
    
    def __init__(self, file_id, version_id):
        self.file_id = file_id
        self.version_id = version_id


class FileTag(db.Model):
    __tablename__ = 'file_tag'
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    file_id = Column(Integer, ForeignKey('file.id'), primary_key=True)

    def __init__(self, file_id, tag_id):
        self.file_id = file_id
        self.tag_id = tag_id


class Type(db.Model):
    __tablename__ = 'type'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False)

    def __init__(self, type):
        self.type = type
    
    def __repr__(self):
            return '{}'.format(self.type)


class TypeForm(FlaskForm):
    type = StringField('Type of File', validators=[DataRequired()])

        
class TypeUser(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100))
    user_ids = relationship('User', backref='user_type', lazy=True)
    
    def __init__(self, type, user_ids):
        self.type = type
        self.user_ids = user_ids
    
    def __repr__(self):
            return '{}'.format(self.type)


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    user_type_id = Column(Integer, ForeignKey(TypeUser.id), nullable=False)
    name = Column(String(50), nullable=False)
    password_hash = Column(String(100), nullable=False)
 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, name, email, user_type_id, password):
        self.name = name
        self.email = email
        self.user_type_id = user_type_id
        self.password_hash = generate_password_hash(password)
    
    def __repr__(self):
            return '{}'.format(self.name)


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    user_types = TypeUser.query.all()
    list = []
    for user_type in user_types:
        list.append((user_type.id, user_type.type))
    user_type_id = SelectField('User Type', choices=list)
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add User')
        

class Version(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False)
    datetime_cr = Column(DateTime, default=datetime.utcnow())
    # file_ids = relationship('FileVersion', primaryjoin=(FileVersion.version_id == id), 
    #                         secondaryjoin=(FileVersion.file_id == File.id),
    #                         backref=db.backref('file_version', lazy='dynamic'), lazy='dynamic')
    hash = Column(String(32))

    def __init__(self, version):
        self.version = version
        self.datetime_cr = datetime.utcnow()

    def __repr__(self):
            return '{}'.format(self.version)

        
class VersionForm(FlaskForm):
    version = StringField('Version', validators=[DataRequired()])
    submit = SubmitField('Add Tag')

        
class Tag(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(100), nullable=False)
    number = Column(Integer)
    # file_ids = relationship('FileTag', secondary='file_tag')
    
    def __init__(self, tag, number):
        self.tag = tag
        self.number = number
    
    def __repr__(self):
            return '{}'.format(self.tag)

        
class TagForm(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired()])
    number = IntegerField('Number')
    submit = SubmitField('Add Tag')


class File(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    type_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    # version_ids = relationship('FileVersion', secondary='file_version')
    # tag_ids = relationship('FileTag', secondary='file_tag')
    file = Column(String)
    
    def __init__(self, name, user_id, type_id, file):
        self.name = name
        self.user_id = user_id
        self.type_id = type_id
        # self.version_ids = version_ids
        self.file = file

    def __repr__(self):
            return '{}'.format(self.name)


class FileForm(FlaskForm):
    tags = Tag.query.all()
    list = []
    for tag in tags:
        list.append((tag.id, tag.tag))
        
    users = User.query.all()
    list1 = []
    for user in users:
        list1.append((user.id, user.name))
        
    types = Type.query.all()
    list2 = []
    list3 = []
    for i in range(100):
        list3.append((i, i))
    
    for type in types:
        list2.append((type.id, type.type))
    name = StringField('Name', validators=[DataRequired()])
    user_id = SelectField('User', choices=list1)
    type_id = SelectField('Type', choices=list2)
    version = SelectField('ver', choices=list3)
    file = FileField('File')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
if __name__ == "__main__":
    db.create_all()

