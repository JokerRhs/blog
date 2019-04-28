

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

u_c =db.Table(
    'u_c',
    db.Column('u_id', db.Integer, db.ForeignKey('user.us_id')),
    db.Column('c_id', db.Integer, db.ForeignKey('cate.cate_id'))

)


class User(db.Model):
    us_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30), nullable=False)
    us_num = db.Column(db.String(50), unique=True)
    us_register_time = db.Column(db.DateTime)
    cate = db.relationship('Category', secondary=u_c, backref='user', lazy=True)
    __tablename__ = 'user'


    def update(self, name, pwd, num, r_time):
        self.username = name
        self.password = pwd
        self.us_num = num
        self.us_register_time = r_time
        db.session.commit()


    def save_update(self, num, pwd, name, r_time):
        self.username = name
        self.password = pwd
        self.us_num = num
        self.us_register_time = r_time
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_title = db.Column(db.String(30), nullable=False)
    art_content = db.Column(db.Text)
    art_des = db.Column(db.String(200))
    art_tag = db.Column(db.String(50))
    art_time = db.Column(db.DateTime, nullable=False)
    art_vis = db.Column(db.Integer, nullable=False)
    art_titlepic = db.Column(db.LargeBinary(length=2048))
    cate_id = db.Column(db.Integer, db.ForeignKey('cate.cate_id'), nullable=True)
    com_id = db.Column(db.Integer, db.ForeignKey('com.com_id'))


    def update(self, title, content, des, tag, time, vis, cate_id=0, titlepic=None):
        self.art_title = title
        self.art_des = des
        self.art_tag = tag
        self.art_time = time
        self.art_vis = vis
        self.art_titlepic = titlepic
        self.art_content = content
        self.cate_id = cate_id
        db.session.commit()

    def save_update(self, title, content, des, tag, time, vis, cate_id=0, titlepic=None):
        self.art_title = title
        self.art_des = des
        self.art_tag = tag
        self.art_time = time
        self.art_vis = vis
        self.art_titlepic = titlepic
        self.art_content = content
        self.cate_id = cate_id
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    __tablename__='art'

class Category(db.Model):
    cate_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cate_name = db.Column(db.String(30), unique=True, nullable=False)
    cate_sec_name = db.Column(db.String(30), unique=True)
    cate_time = db.Column(db.DateTime, nullable=False)
    cate_text = db.Column(db.Text)
    art = db.relationship('Article', backref='cate')


    def update(self, name, sec, time, text):
        self.cate_text = text
        self.cate_sec_name = sec
        self.cate_name = name
        self.cate_time =time
        db.session.commit()

    def save_update(self, name, sec, time, text):
        self.cate_text = text
        self.cate_sec_name = sec
        self.cate_name = name
        self.cate_time = time
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    __tablename__='cate'



class Comment(db.Model):
    com_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    com_content = db.Column(db.Text)
    com_name = db.Column(db.String(50), nullable=False)
    com_time = db. Column(db.DateTime, nullable=False)
    art = db.relationship('Article', backref='com' )


    def update(self, content, time, name='游侠'):
        self.com_time = time
        self.com_name = name
        self.com_content = content
        db.session.commit()

    def save_update(self, content, name, time):
        self.com_time = time
        self.com_name = name
        self.com_content = content
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    __tablename__='com'

